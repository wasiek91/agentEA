"""Portfolio Manager Pro - Main Orchestrator.
Central control hub for all trading operations.
"""
import argparse
import logging
import asyncio
from typing import List, Optional
from datetime import datetime, timedelta
from pathlib import Path

# Core modules
from config import settings
from database import Database, initialize_database
from mt5_connector import MT5Manager
from strategy_framework import StrategyExecutor, StrategyRegistry
from risk_manager import RiskManager, PositionManager
from rl_engine import RLTrainer, RLAgent
from backtester import Backtester
from logging_system import AuditLogger, PerformanceLogger, setup_logging

# Setup logging
logger = setup_logging(log_level='INFO', log_file='portfolio_manager.log')


class PortfolioManagerPro:
    """Main orchestrator for Portfolio Manager Pro."""

    def __init__(self, mode: str = 'live'):
        """Initialize portfolio manager.

        Args:
            mode: 'live', 'paper', 'backtest', or 'rl_training'
        """
        self.mode = mode
        self.db = Database()
        self.mt5 = MT5Manager()
        self.strategy_executor = StrategyExecutor()
        self.risk_manager = RiskManager()
        self.position_manager = PositionManager()
        self.audit_logger = AuditLogger(self.db)
        self.performance_logger = PerformanceLogger()

        logger.info(f"🚀 Portfolio Manager Pro initialized in {mode.upper()} mode")

    def run_live_trading(self, symbols: Optional[List[str]] = None, update_interval_seconds: int = 60):
        """Run live trading mode.

        Args:
            symbols: List of symbols to trade (default: XAUUSD, NASDAQ)
            update_interval_seconds: Strategy execution interval
        """
        symbols = symbols or settings.SYMBOLS
        logger.info(f"📊 Starting live trading on {symbols}...")

        iteration = 0
        try:
            while True:
                iteration += 1
                logger.info(f"\n{'='*60}")
                logger.info(f"Iteration {iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                # 1. Fetch market data
                market_data = {}
                for symbol in symbols:
                    candles = self.mt5.get_candles(symbol, settings.DEFAULT_TIMEFRAME, num_candles=500)
                    if candles:
                        market_data[symbol] = candles
                        logger.info(f"✅ Fetched {len(candles)} candles for {symbol}")

                if not market_data:
                    logger.warning("⚠️  No market data fetched")
                    continue

                # 2. Execute strategies
                signals = self.strategy_executor.execute_round(market_data)
                logger.info(f"📈 Strategy execution: {len(signals['signals'])} signals generated")

                for signal in signals['signals']:
                    self.audit_logger.log_strategy_signal(signal)

                # 3. Process signals & validate trades
                for signal in signals['signals']:
                    symbol = signal['symbol']
                    signal_type = signal['signal']

                    if signal_type == 'HOLD':
                        continue

                    # Get current price
                    price_info = self.mt5.get_current_price(symbol)
                    if not price_info:
                        continue

                    entry_price = price_info['ask'] if signal_type == 'BUY' else price_info['bid']

                    # Validate trade
                    is_valid, validation_msg = self.risk_manager.validate_trade(
                        symbol=symbol,
                        direction=signal_type,
                        lot_size=1.0,
                        entry_price=entry_price
                    )

                    self.audit_logger.log_risk_check({
                        'symbol': symbol,
                        'check_type': 'trade_validation',
                        'current_value': entry_price,
                        'limit_value': self.risk_manager.current_equity,
                        'passed': is_valid,
                        'message': validation_msg
                    })

                    if not is_valid:
                        logger.warning(f"❌ Trade rejected for {symbol}: {validation_msg}")
                        continue

                    # Execute trade
                    logger.info(f"🎯 Executing {signal_type} signal for {symbol} @ {entry_price:.2f}")

                    order_ticket = self.mt5.place_order(
                        symbol=symbol,
                        action=signal_type,
                        lot_size=1.0,
                        price=entry_price,
                        take_profit=entry_price + (50 if signal_type == 'BUY' else -50),
                        stop_loss=entry_price - (50 if signal_type == 'BUY' else -50),
                        comment="PM_Pro_Live"
                    )

                    if order_ticket:
                        self.audit_logger.log_trade({
                            'symbol': symbol,
                            'direction': signal_type,
                            'entry_price': entry_price,
                            'lot_size': 1.0,
                            'reason': f"Signal confidence: {signal['confidence']:.1%}"
                        })

                # 4. Update positions
                positions = self.mt5.get_open_positions()
                logger.info(f"📍 Open positions: {len(positions)}")

                # 5. Log performance snapshot
                self.performance_logger.log_hourly_snapshot()

                # 6. Check stop conditions
                if self.risk_manager.check_stop_conditions():
                    logger.error("🛑 STOP CONDITIONS MET - Halting trading")
                    break

                # Wait for next iteration
                logger.info(f"⏳ Next execution in {update_interval_seconds}s...")
                asyncio.run(asyncio.sleep(update_interval_seconds))

        except KeyboardInterrupt:
            logger.info("🛑 Trading stopped by user")
        except Exception as e:
            logger.error(f"❌ Error in live trading: {e}")
            self.audit_logger.log_error({
                'actor': 'LiveTradingLoop',
                'message': str(e),
                'error_type': type(e).__name__,
                'context': {'mode': self.mode, 'iteration': iteration}
            })

    def run_paper_trading(self, symbols: Optional[List[str]] = None, days: int = 30):
        """Run paper trading (simulation).

        Args:
            symbols: List of symbols to trade
            days: Number of days to simulate
        """
        symbols = symbols or settings.SYMBOLS
        logger.info(f"📋 Starting paper trading on {symbols} for {days} days...")

        backtester = Backtester(
            start_date=datetime.now() - timedelta(days=days),
            end_date=datetime.now()
        )

        for symbol in symbols:
            registry = StrategyRegistry()
            for strategy_id, strategy in registry.strategies.items():
                if strategy.symbol != symbol:
                    continue

                result = backtester.backtest_strategy(strategy, symbol)
                metrics = result.calculate_metrics()

                logger.info(f"\n✅ Paper Trading Results for {strategy.name}:")
                logger.info(f"  Total Trades: {metrics['total_trades']}")
                logger.info(f"  Win Rate: {metrics['win_rate']:.1%}")
                logger.info(f"  Total Profit: ${metrics['total_profit']:.2f}")
                logger.info(f"  Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
                logger.info(f"  Max Drawdown: {metrics['max_drawdown']:.2f}%")

    def run_rl_training(self, symbols: Optional[List[str]] = None, timesteps: int = 50000):
        """Run RL agent training.

        Args:
            symbols: List of symbols to train on
            timesteps: Training timesteps per symbol
        """
        symbols = symbols or [settings.SYMBOLS[0]]
        logger.info(f"🤖 Starting RL training on {symbols}...")

        trainer = RLTrainer(symbols=symbols, model_type=settings.RL_MODEL_TYPE)
        trainer.train_all(total_timesteps=timesteps)

        logger.info("✅ RL training completed")

    def run_backtest(self, strategy_name: str, symbol: str, start_date: Optional[str] = None,
                    end_date: Optional[str] = None):
        """Run full backtest on strategy.

        Args:
            strategy_name: Strategy name to backtest
            symbol: Trading symbol
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        """
        logger.info(f"📊 Backtesting {strategy_name} on {symbol}...")

        # Parse dates
        start = datetime.strptime(start_date, '%Y-%m-%d') if start_date else datetime.now() - timedelta(days=365)
        end = datetime.strptime(end_date, '%Y-%m-%d') if end_date else datetime.now()

        backtester = Backtester(start_date=start, end_date=end)
        registry = StrategyRegistry()

        # Find strategy
        target_strategy = None
        for strategy_id, strategy in registry.strategies.items():
            if strategy.name == strategy_name and strategy.symbol == symbol:
                target_strategy = strategy
                break

        if not target_strategy:
            logger.error(f"❌ Strategy {strategy_name} not found")
            return

        # Run backtest
        result = backtester.backtest_strategy(target_strategy, symbol, start, end)
        metrics = result.calculate_metrics()

        # Display report
        from backtester import BacktestReporter
        report = BacktestReporter.generate_report(result, strategy_name)
        print(report)

        logger.info("✅ Backtest completed")

    def optimize_strategy(self, strategy_name: str, symbol: str):
        """Optimize strategy parameters.

        Args:
            strategy_name: Strategy to optimize
            symbol: Trading symbol
        """
        logger.info(f"🔍 Optimizing {strategy_name} on {symbol}...")

        backtester = Backtester()

        # Define parameter ranges
        if strategy_name == "RSI":
            param_ranges = {
                'period': [10, 12, 14, 16, 18],
                'overbought': [65, 70, 75],
                'oversold': [25, 30, 35]
            }
        elif strategy_name == "MA":
            param_ranges = {
                'fast': [3, 5, 7, 10],
                'slow': [15, 20, 25, 30]
            }
        else:
            logger.error(f"❌ Unknown strategy: {strategy_name}")
            return

        # Find strategy class
        from strategy_framework import RSIStrategy, MAStrategyStrategy
        strategy_classes = {
            'RSI': RSIStrategy,
            'MA': MAStrategyStrategy
        }

        best_params, best_value = backtester.optimize_parameters(
            strategy_class=strategy_classes[strategy_name],
            symbol=symbol,
            param_ranges=param_ranges,
            optimization_metric='sharpe_ratio'
        )

        logger.info(f"✅ Best parameters: {best_params}")
        logger.info(f"   Sharpe Ratio: {best_value:.2f}")

    def get_status(self):
        """Get system status."""
        metrics = self.risk_manager.get_risk_metrics()
        positions = self.mt5.get_open_positions()

        status = f"""
╔════════════════════════════════════════════════════════════╗
║          PORTFOLIO MANAGER PRO - STATUS REPORT             ║
╚════════════════════════════════════════════════════════════╝

📊 SYSTEM STATUS
─────────────────────────────────────────
Mode: {self.mode.upper()}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
MT5 Connected: ✅ Yes

💰 ACCOUNT METRICS
─────────────────────────────────────────
Current Equity: ${metrics['current_equity']:,.2f}
Current Drawdown: {metrics['current_drawdown']:.2f}%
Drawdown Level: {metrics['drawdown_level']}
Daily Loss: {metrics['daily_loss_pct']:.2f}%

📍 POSITIONS
─────────────────────────────────────────
Open Positions: {metrics['open_positions']}
Total Position Value: ${metrics['total_position_value']:,.2f}
Margin Utilization: {metrics['margin_utilization']:.2f}%

📈 STRATEGIES
─────────────────────────────────────────
Active Strategies: {len(self.strategy_executor.registry.strategies)}
"""

        if len(positions) > 0:
            status += "\n🔍 OPEN POSITIONS:\n"
            for pos in positions[:5]:
                status += f"  • {pos['symbol']} {pos['type']}: {pos['volume']} lots @ {pos['open_price']:.2f}\n"

        status += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return status


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Portfolio Manager Pro - Trading Bot')

    parser.add_argument('--mode', choices=['live', 'paper', 'backtest', 'rl', 'status'],
                       default='live', help='Execution mode')
    parser.add_argument('--symbols', nargs='+', default=None, help='Trading symbols')
    parser.add_argument('--days', type=int, default=30, help='Backtest/paper trading days')
    parser.add_argument('--timesteps', type=int, default=50000, help='RL training timesteps')
    parser.add_argument('--strategy', default=None, help='Strategy name for optimization')
    parser.add_argument('--symbol', default='XAUUSD', help='Symbol for backtest/optimization')
    parser.add_argument('--start-date', default=None, help='Backtest start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', default=None, help='Backtest end date (YYYY-MM-DD)')

    args = parser.parse_args()

    # Initialize
    try:
        initialize_database()
        manager = PortfolioManagerPro(mode=args.mode)

        # Route to appropriate mode
        if args.mode == 'live':
            manager.run_live_trading(symbols=args.symbols)

        elif args.mode == 'paper':
            manager.run_paper_trading(symbols=args.symbols, days=args.days)

        elif args.mode == 'rl':
            manager.run_rl_training(symbols=args.symbols, timesteps=args.timesteps)

        elif args.mode == 'backtest':
            if not args.strategy:
                logger.error("--strategy required for backtest mode")
                return
            manager.run_backtest(args.strategy, args.symbol, args.start_date, args.end_date)

        elif args.mode == 'status':
            print(manager.get_status())

    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
