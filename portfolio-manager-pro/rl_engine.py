"""Reinforcement Learning Engine - Self-Optimizing Trading Agent."""
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
import logging
from config import settings
from database import Database
from strategy_framework import StrategyExecutor
import ta
from datetime import datetime, timedelta

# Stable-Baselines3
from stable_baselines3 import DQN, PPO, A2C
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback, BaseCallback

logger = logging.getLogger(__name__)


class SharpeEarlyStoppingCallback(BaseCallback):
    """Early stopping callback based on Sharpe ratio threshold."""

    def __init__(self, sharpe_threshold: float = 1.0, check_freq: int = 10000, verbose: int = 0):
        """Initialize callback.

        Args:
            sharpe_threshold: Target Sharpe ratio to achieve
            check_freq: Frequency (in timesteps) to evaluate Sharpe
            verbose: Verbosity level
        """
        super().__init__(verbose)
        self.sharpe_threshold = sharpe_threshold
        self.check_freq = check_freq
        self.episode_rewards = []
        self.best_sharpe = -np.inf

    def _on_step(self) -> bool:
        """Called at each step. Returns False to stop training."""
        # Collect episode rewards
        if len(self.locals.get("infos", [])) > 0:
            for info in self.locals["infos"]:
                if "episode" in info:
                    ep_reward = info["episode"]["r"]
                    self.episode_rewards.append(ep_reward)

        # Check Sharpe every check_freq steps
        if self.n_calls % self.check_freq == 0 and len(self.episode_rewards) >= 30:
            recent_rewards = self.episode_rewards[-30:]
            mean_reward = np.mean(recent_rewards)
            std_reward = np.std(recent_rewards)

            if std_reward > 0:
                sharpe_ratio = mean_reward / std_reward
            else:
                sharpe_ratio = 0

            if sharpe_ratio > self.best_sharpe:
                self.best_sharpe = sharpe_ratio
                logger.info(f"🎯 New best Sharpe ratio: {sharpe_ratio:.3f} at step {self.n_calls}")

            if sharpe_ratio >= self.sharpe_threshold:
                logger.info(f"✅ Target Sharpe {self.sharpe_threshold:.2f} achieved! Stopping training.")
                return False  # Stop training

        return True  # Continue training


class TradingEnvironment(gym.Env):
    """Gymnasium environment for trading."""

    metadata = {"render_modes": ["human"]}

    def __init__(self, symbol: str = "XAUUSD", timeframe: int = 60, lookback: int = 100):
        """Initialize trading environment.

        Args:
            symbol: Trading symbol (XAUUSD, NASDAQ, etc.)
            timeframe: Candle timeframe in minutes
            lookback: Number of historical candles to load
        """
        super().__init__()

        self.symbol = symbol
        self.timeframe = timeframe
        self.lookback = lookback
        self.db = Database()
        self.executor = StrategyExecutor()

        # Market data
        self.candles = []
        self.current_idx = 0
        self.initial_balance = settings.INITIAL_CAPITAL
        self.current_balance = self.initial_balance
        self.equity = self.initial_balance
        self.peak_equity = self.initial_balance
        self.drawdown = 0

        # Position tracking
        self.open_position = None  # {'direction': 'BUY'|'SELL', 'entry_price': float, 'size': float}
        self.position_history = []
        self.win_count = 0
        self.loss_count = 0

        # State space: [price, RSI, MACD, volume, equity, drawdown, position_size,
        #               ATR, win_rate, sharpe_estimate, max_drawdown]
        # Normalized to [0, 1] range
        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(11,),
            dtype=np.float32
        )

        # Action space: 0=HOLD, 1=BUY_SMALL, 2=BUY_MEDIUM, 3=BUY_LARGE,
        #              4=SELL_SMALL, 5=SELL_MEDIUM, 6=SELL_LARGE, 7=CLOSE
        self.action_space = spaces.Discrete(8)

        self.action_map = {
            0: {'action': 'HOLD', 'size': 0},
            1: {'action': 'BUY', 'size': 0.1},
            2: {'action': 'BUY', 'size': 0.25},
            3: {'action': 'BUY', 'size': 0.5},
            4: {'action': 'SELL', 'size': 0.1},
            5: {'action': 'SELL', 'size': 0.25},
            6: {'action': 'SELL', 'size': 0.5},
            7: {'action': 'CLOSE', 'size': 1.0},
        }

        # Load market data
        self._load_market_data()

    def _load_market_data(self):
        """Load historical market data from database."""
        try:
            self.candles = self.db.get_candles(self.symbol, self.timeframe, self.lookback)
            if len(self.candles) < 20:
                logger.warning(f"⚠️  Only {len(self.candles)} candles loaded, need at least 20")
            logger.info(f"✅ Loaded {len(self.candles)} candles for {self.symbol}")
        except Exception as e:
            logger.error(f"❌ Failed to load market data: {e}")
            self.candles = pd.DataFrame()

    def _calculate_indicators(self) -> Dict:
        """Calculate technical indicators for current state."""
        if self.current_idx < 20:
            return {
                'price': 0,
                'rsi': 50,
                'macd': 0,
                'volume': 0,
                'atr': 0
            }

        lookback_candles = self.candles.iloc[max(0, self.current_idx - 20):self.current_idx + 1]
        close = lookback_candles['close'].values
        high = lookback_candles['high'].values
        low = lookback_candles['low'].values
        volume = lookback_candles['volume'].values

        # RSI (14-period)
        rsi = ta.momentum.rsi(pd.Series(close), length=14).values[-1]
        if pd.isna(rsi):
            rsi = 50

        # MACD
        macd_result = ta.trend.macd(pd.Series(close))
        if len(macd_result) > 0:
            macd = macd_result.iloc[-1] if hasattr(macd_result, 'iloc') else float(macd_result[-1])
            if pd.isna(macd):
                macd = 0
        else:
            macd = 0

        # ATR (14-period) for volatility
        atr = ta.volatility.atr(pd.Series(high), pd.Series(low), pd.Series(close), length=14).values[-1]
        if pd.isna(atr):
            atr = 0

        return {
            'price': float(close[-1]),
            'rsi': float(rsi),
            'macd': float(macd),
            'volume': float(volume[-1]) if len(volume) > 0 else 0,
            'atr': float(atr)
        }

    def _get_state(self) -> np.ndarray:
        """Get normalized state vector."""
        indicators = self._calculate_indicators()

        # Get current price
        if self.current_idx >= len(self.candles):
            current_price = self.candles.iloc[-1]['close']
        else:
            current_price = self.candles.iloc[self.current_idx]['close']

        # Normalize state values to [0, 1]
        price_norm = min(indicators['price'] / 10000, 1.0)  # Assume max price ~10k
        rsi_norm = indicators['rsi'] / 100.0
        macd_norm = max(min(indicators['macd'] / 100, 1.0), 0.0)
        volume_norm = min(indicators['volume'] / 1000000, 1.0)  # Assume max volume
        equity_norm = self.equity / self.initial_balance
        drawdown_norm = min(self.drawdown / 50, 1.0)  # Max 50% drawdown
        position_size_norm = (self.open_position['size'] / 1.0) if self.open_position else 0.0

        # New features
        atr_norm = min(indicators['atr'] / 100, 1.0)  # Volatility indicator

        # Win rate (last 20 trades)
        if len(self.position_history) > 0:
            recent_trades = min(20, len(self.position_history))
            recent_wins = sum(1 for pos in self.position_history[-recent_trades:] if pos['pnl'] > 0)
            win_rate_norm = recent_wins / recent_trades
        else:
            win_rate_norm = 0.5  # Neutral

        # Sharpe estimate (rolling)
        if len(self.position_history) >= 10:
            recent_pnls = [pos['pnl'] for pos in self.position_history[-10:]]
            mean_pnl = np.mean(recent_pnls)
            std_pnl = np.std(recent_pnls)
            sharpe_estimate = (mean_pnl / std_pnl) if std_pnl > 0 else 0
            sharpe_norm = max(min((sharpe_estimate + 2) / 4, 1.0), 0.0)  # Scale from [-2, 2] to [0, 1]
        else:
            sharpe_norm = 0.5  # Neutral

        # Max drawdown seen this session
        max_dd_norm = min(self.drawdown / 20, 1.0)  # Scale to 20% max

        state = np.array([
            price_norm,
            rsi_norm,
            macd_norm,
            volume_norm,
            equity_norm,
            drawdown_norm,
            position_size_norm,
            atr_norm,
            win_rate_norm,
            sharpe_norm,
            max_dd_norm
        ], dtype=np.float32)

        return state

    def _calculate_reward(self, action: int, price_before: float, price_after: float) -> float:
        """Calculate reward for action - Sharpe-optimized.

        Reward = Sharpe ratio component + profit - risk_penalty - transaction_cost
        """
        reward = 0.0

        # If holding a position, calculate profit/loss
        if self.open_position:
            price_change = price_after - price_before

            if self.open_position['direction'] == 'BUY':
                pnl = price_change * self.open_position['size']
            else:  # SELL
                pnl = -price_change * self.open_position['size']

            reward += pnl / 100  # Normalize profit

            # Drawdown penalty (progressive)
            if self.drawdown > 0:
                reward -= (self.drawdown / 100) ** 2  # Quadratic penalty

            # Close position reward
            if action == 7 and pnl > 0:
                reward += 1.0  # Bonus for closing winning position
            elif action == 7 and pnl < 0:
                reward -= 0.5  # Penalty for closing losing position

        # Sharpe ratio component (rolling window)
        if len(self.position_history) >= 10:
            recent_pnls = [pos['pnl'] for pos in self.position_history[-10:]]
            mean_pnl = np.mean(recent_pnls)
            std_pnl = np.std(recent_pnls)

            if std_pnl > 0:
                sharpe_estimate = mean_pnl / std_pnl
                reward += sharpe_estimate * 0.5  # Sharpe bonus
            else:
                reward += 0.1  # Small bonus for zero volatility (all wins/losses equal)

        # Win rate bonus
        if len(self.position_history) > 0:
            win_rate = self.win_count / (self.win_count + self.loss_count) if (self.win_count + self.loss_count) > 0 else 0
            reward += win_rate * 0.1

        # Transaction cost penalty (discourage overtrading)
        if action in [1, 2, 3, 4, 5, 6]:  # Opening position
            reward -= 0.05  # Small cost per trade

        return reward

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        """Execute one step in environment.

        Returns: observation, reward, terminated, truncated, info
        """
        if self.current_idx >= len(self.candles) - 1:
            return self._get_state(), 0, True, False, {'reason': 'End of data'}

        # Get price before action
        price_before = self.candles.iloc[self.current_idx]['close']

        # Move to next candle
        self.current_idx += 1
        price_after = self.candles.iloc[self.current_idx]['close']

        # Execute action
        action_info = self.action_map[action]
        reward = 0

        if action_info['action'] == 'HOLD':
            # Update existing position if open
            if self.open_position:
                if self.open_position['direction'] == 'BUY':
                    pnl = (price_after - self.open_position['entry_price']) * self.open_position['size']
                else:
                    pnl = (self.open_position['entry_price'] - price_after) * self.open_position['size']

                self.equity = self.initial_balance + pnl
                reward = pnl / 1000  # Normalize

        elif action_info['action'] == 'BUY' and not self.open_position:
            size = action_info['size']
            self.open_position = {
                'direction': 'BUY',
                'entry_price': price_after,
                'size': size
            }
            reward = 0.1

        elif action_info['action'] == 'SELL' and not self.open_position:
            size = action_info['size']
            self.open_position = {
                'direction': 'SELL',
                'entry_price': price_after,
                'size': size
            }
            reward = 0.1

        elif action_info['action'] == 'CLOSE' and self.open_position:
            # Calculate P&L
            if self.open_position['direction'] == 'BUY':
                pnl = (price_after - self.open_position['entry_price']) * self.open_position['size']
            else:
                pnl = (self.open_position['entry_price'] - price_after) * self.open_position['size']

            self.equity = self.initial_balance + pnl

            if pnl > 0:
                self.win_count += 1
                reward = 1.0
            elif pnl < 0:
                self.loss_count += 1
                reward = -1.0

            self.position_history.append({
                'entry_price': self.open_position['entry_price'],
                'exit_price': price_after,
                'direction': self.open_position['direction'],
                'pnl': pnl
            })

            self.open_position = None

        # Update drawdown
        if self.equity < self.peak_equity:
            self.drawdown = ((self.peak_equity - self.equity) / self.peak_equity) * 100
        else:
            self.peak_equity = self.equity
            self.drawdown = 0

        # Check termination conditions
        terminated = self.current_idx >= len(self.candles) - 1
        truncated = self.drawdown > settings.DRAWDOWN_CRITICAL

        return self._get_state(), reward, terminated, truncated, {
            'price': price_after,
            'equity': self.equity,
            'drawdown': self.drawdown,
            'position': self.open_position
        }

    def reset(self, seed=None) -> Tuple[np.ndarray, Dict]:
        """Reset environment to initial state."""
        super().reset(seed=seed)

        self.current_idx = 20  # Start after enough data for indicators
        self.current_balance = self.initial_balance
        self.equity = self.initial_balance
        self.peak_equity = self.initial_balance
        self.drawdown = 0
        self.open_position = None
        self.position_history = []
        self.win_count = 0
        self.loss_count = 0

        return self._get_state(), {}

    def render(self, mode='human'):
        """Render environment state."""
        if mode == 'human':
            print(f"Step: {self.current_idx}, Equity: ${self.equity:,.2f}, Drawdown: {self.drawdown:.2f}%")


class RLAgent:
    """Manages RL model training and inference."""

    def __init__(self, symbol: str = "XAUUSD", model_type: str = "PPO", model_version: str = "v1"):
        """Initialize RL Agent.

        Args:
            symbol: Trading symbol
            model_type: 'DQN', 'PPO', or 'A2C'
            model_version: Model version identifier
        """
        self.symbol = symbol
        self.model_type = model_type
        self.model_version = model_version
        self.db = Database()
        self.env = None
        self.model = None
        self.best_reward = -np.inf

    def create_environment(self, symbol: str = "XAUUSD") -> TradingEnvironment:
        """Create trading environment."""
        env = TradingEnvironment(symbol=symbol, timeframe=60, lookback=100)
        self.env = env
        return env

    def build_model(self, env: gym.Env, learning_rate: float = 0.0003):
        """Build and compile RL model.

        Args:
            env: Gymnasium environment
            learning_rate: Learning rate for optimizer
        """
        try:
            if self.model_type == "DQN":
                self.model = DQN(
                    "MlpPolicy",
                    env,
                    learning_rate=learning_rate,
                    buffer_size=10000,
                    learning_starts=1000,
                    exploration_fraction=0.1,
                    exploration_initial_eps=1.0,
                    exploration_final_eps=0.05,
                    verbose=1
                )
            elif self.model_type == "PPO":
                self.model = PPO(
                    "MlpPolicy",
                    env,
                    learning_rate=learning_rate,
                    n_steps=512,  # Reduced for faster adaptation (forex needs quick response)
                    batch_size=128,  # Increased for stable updates
                    n_epochs=20,  # More epochs for better convergence
                    gamma=0.97,  # Slightly lower - prioritize recent rewards
                    gae_lambda=0.95,  # Generalized Advantage Estimation
                    clip_range=0.2,  # PPO clipping
                    ent_coef=0.01,  # Entropy bonus for exploration
                    vf_coef=0.5,  # Value function coefficient
                    max_grad_norm=0.5,  # Gradient clipping
                    verbose=1
                )
            elif self.model_type == "A2C":
                self.model = A2C(
                    "MlpPolicy",
                    env,
                    learning_rate=learning_rate,
                    verbose=1
                )
            else:
                raise ValueError(f"Unknown model type: {self.model_type}")

            logger.info(f"✅ {self.model_type} model created for {self.symbol}")
            return self.model

        except Exception as e:
            logger.error(f"❌ Failed to build model: {e}")
            raise

    def train(self, total_timesteps: int = 50000, eval_episodes: int = 5, sharpe_target: float = 1.0):
        """Train RL model.

        Args:
            total_timesteps: Total training steps
            eval_episodes: Episodes between evaluations
            sharpe_target: Target Sharpe ratio for early stopping
        """
        try:
            if not self.env:
                self.create_environment(self.symbol)

            if not self.model:
                self.build_model(self.env, learning_rate=settings.RL_LEARNING_RATE)

            # Callbacks
            checkpoint_callback = CheckpointCallback(
                save_freq=10000,
                save_path=f"./models/{self.model_version}/",
                name_prefix=f"rl_model_{self.symbol}"
            )

            # Early stopping based on Sharpe ratio
            sharpe_callback = SharpeEarlyStoppingCallback(
                sharpe_threshold=sharpe_target,
                check_freq=5000,
                verbose=1
            )

            logger.info(f"🤖 Starting training: {self.model_type} for {total_timesteps} steps...")
            logger.info(f"🎯 Target Sharpe ratio: {sharpe_target:.2f}")

            # Train
            self.model.learn(
                total_timesteps=total_timesteps,
                callback=[checkpoint_callback, sharpe_callback],
                progress_bar=True
            )

            logger.info(f"✅ Training completed")

            # Save final model
            self.model.save(f"./models/{self.model_version}/final_model_{self.symbol}")
            logger.info(f"✅ Model saved: ./models/{self.model_version}/final_model_{self.symbol}")

        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            raise

    def predict(self, state: np.ndarray) -> Tuple[int, np.ndarray]:
        """Predict action for given state.

        Args:
            state: Current environment state

        Returns: action, logits
        """
        try:
            action, _states = self.model.predict(state, deterministic=True)
            return int(action), _states
        except Exception as e:
            logger.error(f"❌ Prediction failed: {e}")
            return 0, None  # HOLD action

    def save_checkpoint(self, episode: int, reward: float):
        """Save model checkpoint with reward tracking.

        Args:
            episode: Training episode number
            reward: Episode reward
        """
        try:
            self.model.save(f"./models/{self.model_version}/checkpoint_ep{episode}_{self.symbol}")
            self.db.log_rl_training(episode, reward, reward, self.model_version)

            if reward > self.best_reward:
                self.best_reward = reward
                self.model.save(f"./models/{self.model_version}/best_model_{self.symbol}")
                logger.info(f"🎯 New best model: Episode {episode}, Reward: {reward:.2f}")

        except Exception as e:
            logger.error(f"❌ Failed to save checkpoint: {e}")

    def load_model(self, model_path: str):
        """Load pre-trained model.

        Args:
            model_path: Path to saved model
        """
        try:
            if self.model_type == "DQN":
                self.model = DQN.load(model_path)
            elif self.model_type == "PPO":
                self.model = PPO.load(model_path)
            elif self.model_type == "A2C":
                self.model = A2C.load(model_path)

            logger.info(f"✅ Model loaded: {model_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            raise


class RLTrainer:
    """Orchestrates RL training pipeline."""

    def __init__(self, symbols: List[str] = None, model_type: str = "PPO"):
        """Initialize trainer.

        Args:
            symbols: List of symbols to train on
            model_type: RL model type (DQN, PPO, A2C)
        """
        self.symbols = symbols or [settings.SYMBOLS[0]]
        self.model_type = model_type
        self.db = Database()
        self.agents: Dict[str, RLAgent] = {}

    def train_all(self, total_timesteps: int = 50000):
        """Train agents on all symbols.

        Args:
            total_timesteps: Steps per symbol
        """
        logger.info(f"🚀 Starting RL training for {len(self.symbols)} symbols...")

        for symbol in self.symbols:
            try:
                logger.info(f"\n📊 Training on {symbol}...")

                agent = RLAgent(symbol=symbol, model_type=self.model_type)
                agent.create_environment(symbol)
                agent.build_model(agent.env)
                agent.train(total_timesteps=total_timesteps)

                self.agents[symbol] = agent

            except Exception as e:
                logger.error(f"❌ Training failed for {symbol}: {e}")

        logger.info(f"✅ Training completed for {len(self.agents)} symbols")

    def get_agent(self, symbol: str) -> Optional[RLAgent]:
        """Get trained agent for symbol.

        Args:
            symbol: Trading symbol

        Returns: RLAgent or None
        """
        return self.agents.get(symbol)


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    # Create and test environment
    env = TradingEnvironment(symbol="XAUUSD")
    check_env(env)
    logger.info("✅ Environment is valid")

    # Train agent
    trainer = RLTrainer(symbols=["XAUUSD"], model_type="PPO")
    trainer.train_all(total_timesteps=50000)
