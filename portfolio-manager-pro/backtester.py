"""Backtesting Engine - Historical Simulation & Optimization."""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from config import settings
from database import Database
from strategy_framework import StrategyRegistry, BaseStrategy, RSIStrategy, MAStrategyStrategy
import ta

logger = logging.getLogger(__name__)


class BacktestResult:
    """Container for backtest results."""

    def __init__(self):
        self.trades: List[Dict] = []
        self.equity_curve: List[float] = []
        self.timestamps: List[datetime] = []
        self.daily_returns: List[float] = []
        self.parameters: Dict = {}

    def calculate_metrics(self) -> Dict:
        """Calculate comprehensive performance metrics."""
        if len(self.trades) == 0:
            return self._empty_metrics()

        # Basic stats
        total_trades = len(self.trades)
        winning_trades = [t for t in self.trades if t['profit'] > 0]
        losing_trades = [t for t in self.trades if t['profit'] < 0]

        win_count = len(winning_trades)
        loss_count = len(losing_trades)
        win_rate = win_count / total_trades if total_trades > 0 else 0

        total_profit = sum(t['profit'] for t in self.trades)
        avg_profit = np.mean([t['profit'] for t in self.trades]) if len(self.trades) > 0 else 0
        avg_win = np.mean([t['profit'] for t in winning_trades]) if len(winning_trades) > 0 else 0
        avg_loss = np.mean([t['profit'] for t in losing_trades]) if len(losing_trades) > 0 else 0

        profit_factor = abs(sum(t['profit'] for t in winning_trades) / sum(t['profit'] for t in losing_trades)) if len(losing_trades) > 0 else 0

        # Drawdown analysis
        equity_array = np.array(self.equity_curve)
        peak = np.maximum.accumulate(equity_array)
        drawdown = (peak - equity_array) / peak * 100
        max_drawdown = np.max(drawdown) if len(drawdown) > 0 else 0

        # Return analysis
        returns = np.diff(self.equity_curve) / self.equity_curve[:-1] if len(self.equity_curve) > 1 else np.array([])

        # Sharpe Ratio (assuming 252 trading days/year, ~0% risk-free rate)
        if len(returns) > 0 and np.std(returns) > 0:
            annual_return = np.mean(returns) * 252
            annual_std = np.std(returns) * np.sqrt(252)
            sharpe_ratio = (annual_return - 0.02) / annual_std if annual_std > 0 else 0
        else:
            sharpe_ratio = 0

        # Sortino Ratio (only downside deviation)
        downside_returns = returns[returns < 0]
        if len(downside_returns) > 0:
            downside_std = np.std(downside_returns) * np.sqrt(252)
            sortino_ratio = (annual_return - 0.02) / downside_std if downside_std > 0 else 0
        else:
            sortino_ratio = sharpe_ratio

        # Calmar Ratio (annual return / max drawdown)
        if max_drawdown > 0:
            calmar_ratio = annual_return / (max_drawdown / 100)
        else:
            calmar_ratio = 0

        return {
            'total_trades': total_trades,
            'winning_trades': win_count,
            'losing_trades': loss_count,
            'win_rate': win_rate,
            'total_profit': total_profit,
            'avg_profit': avg_profit,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'calmar_ratio': calmar_ratio,
            'final_equity': self.equity_curve[-1] if len(self.equity_curve) > 0 else 0,
            'return_pct': ((self.equity_curve[-1] - settings.INITIAL_CAPITAL) / settings.INITIAL_CAPITAL * 100) if len(self.equity_curve) > 0 else 0
        }

    def _empty_metrics(self) -> Dict:
        """Return empty metrics."""
        return {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0,
            'total_profit': 0,
            'avg_profit': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'profit_factor': 0,
            'max_drawdown': 0,
            'sharpe_ratio': 0,
            'sortino_ratio': 0,
            'calmar_ratio': 0,
            'final_equity': settings.INITIAL_CAPITAL,
            'return_pct': 0
        }


class Backtester:
    """Backtesting engine for strategy validation."""

    def __init__(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
        """Initialize backtester.

        Args:
            start_date: Backtest start date
            end_date: Backtest end date
        """
        self.db = Database()
        self.start_date = start_date or (datetime.now() - timedelta(days=365))
        self.end_date = end_date or datetime.now()
        self.initial_balance = settings.INITIAL_CAPITAL

    def backtest_strategy(self, strategy: BaseStrategy, symbol: str,
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None) -> BacktestResult:
        """Backtest single strategy.

        Args:
            strategy: Strategy instance to test
            symbol: Trading symbol
            start_date: Override start date
            end_date: Override end date

        Returns: BacktestResult object
        """
        start = start_date or self.start_date
        end = end_date or self.end_date

        logger.info(f"📊 Backtesting {strategy.name} on {symbol} ({start.date()} - {end.date()})")

        # Load historical candles
        candles = self.db.get_candles(symbol, strategy.timeframe, limit=1000)

        if len(candles) == 0:
            logger.warning(f"⚠️  No candles found for {symbol}")
            return BacktestResult()

        # Filter by date range
        candles['timestamp'] = pd.to_datetime(candles['timestamp'])
        candles = candles[(candles['timestamp'] >= start) & (candles['timestamp'] <= end)]

        if len(candles) == 0:
            logger.warning(f"⚠️  No candles in date range")
            return BacktestResult()

        # Run simulation
        result = BacktestResult()
        result.parameters = strategy.config
        equity = self.initial_balance
        peak_equity = equity
        open_position = None

        for idx, row in candles.iterrows():
            # Calculate indicators
            lookback = candles.iloc[max(0, idx - 20):idx + 1]
            indicators = strategy.calculate_indicators(lookback)

            # Generate signal
            signal, confidence = strategy.generate_signal(indicators)

            # Execute logic
            current_price = row['close']

            # Close existing position if signal reverses
            if open_position and signal == 'HOLD':
                # Hold the position
                pass
            elif open_position and signal and signal != open_position['signal']:
                # Reverse position
                if open_position['signal'] == 'BUY':
                    profit = (current_price - open_position['entry_price']) * open_position['size']
                else:  # SELL
                    profit = (open_position['entry_price'] - current_price) * open_position['size']

                equity += profit
                result.trades.append({
                    'entry_price': open_position['entry_price'],
                    'exit_price': current_price,
                    'signal': open_position['signal'],
                    'profit': profit,
                    'timestamp': row['timestamp']
                })

                # Open new position
                if signal != 'HOLD':
                    open_position = {
                        'signal': signal,
                        'entry_price': current_price,
                        'size': 1.0,
                        'entry_time': row['timestamp']
                    }
            elif not open_position and signal and signal != 'HOLD':
                # Open new position
                open_position = {
                    'signal': signal,
                    'entry_price': current_price,
                    'size': 1.0,
                    'entry_time': row['timestamp']
                }

            # Update equity curve
            if open_position:
                if open_position['signal'] == 'BUY':
                    unrealized_pnl = (current_price - open_position['entry_price']) * open_position['size']
                else:  # SELL
                    unrealized_pnl = (open_position['entry_price'] - current_price) * open_position['size']
                current_equity = equity + unrealized_pnl
            else:
                current_equity = equity

            result.equity_curve.append(current_equity)
            result.timestamps.append(row['timestamp'])

            # Update peak for drawdown
            if current_equity > peak_equity:
                peak_equity = current_equity

        # Close final position
        if open_position:
            last_price = candles.iloc[-1]['close']
            if open_position['signal'] == 'BUY':
                profit = (last_price - open_position['entry_price']) * open_position['size']
            else:
                profit = (open_position['entry_price'] - last_price) * open_position['size']

            equity += profit
            result.trades.append({
                'entry_price': open_position['entry_price'],
                'exit_price': last_price,
                'signal': open_position['signal'],
                'profit': profit,
                'timestamp': candles.iloc[-1]['timestamp']
            })

        logger.info(f"✅ Backtest completed: {len(result.trades)} trades")
        return result

    def optimize_parameters(self, strategy_class, symbol: str,
                           param_ranges: Dict[str, List],
                           optimization_metric: str = 'sharpe_ratio') -> Tuple[Dict, float]:
        """Optimize strategy parameters via grid search.

        Args:
            strategy_class: Strategy class to optimize
            symbol: Trading symbol
            param_ranges: Dictionary of parameter ranges to test
            optimization_metric: Metric to optimize ('sharpe_ratio', 'profit_factor', 'win_rate', etc.)

        Returns: (best_parameters, best_metric_value)
        """
        logger.info(f"🔍 Optimizing {strategy_class.__name__} parameters...")

        best_value = -np.inf if optimization_metric != 'max_drawdown' else np.inf
        best_params = {}

        # Generate parameter combinations
        param_names = list(param_ranges.keys())
        param_lists = [param_ranges[name] for name in param_names]

        total_combinations = np.prod([len(p) for p in param_lists])
        combination_count = 0

        # Grid search
        for param_values in self._generate_combinations(param_lists):
            combination_count += 1
            if combination_count % 10 == 0:
                logger.info(f"  Testing combination {combination_count}/{total_combinations}")

            # Create strategy with current parameters
            config = dict(zip(param_names, param_values))
            strategy = strategy_class(
                name=f"opt_{strategy_class.__name__}",
                symbol=symbol,
                timeframe=60,
                config=config
            )

            # Run backtest
            result = self.backtest_strategy(strategy, symbol)
            metrics = result.calculate_metrics()

            # Check if this is better
            metric_value = metrics.get(optimization_metric, 0)

            is_better = False
            if optimization_metric == 'max_drawdown':
                is_better = metric_value < best_value
            else:
                is_better = metric_value > best_value

            if is_better:
                best_value = metric_value
                best_params = config
                logger.info(f"  📈 New best: {optimization_metric}={metric_value:.2f}")

        logger.info(f"✅ Optimization completed: {optimization_metric}={best_value:.2f}")
        return best_params, best_value

    def _generate_combinations(self, param_lists: List[List]) -> List[Tuple]:
        """Generate all parameter combinations."""
        if not param_lists:
            yield []
            return

        for value in param_lists[0]:
            for rest in self._generate_combinations(param_lists[1:]):
                yield [value] + rest

    def walkforward_validation(self, strategy: BaseStrategy, symbol: str,
                             train_period_days: int = 252,
                             test_period_days: int = 63) -> Dict:
        """Walk-forward validation.

        Args:
            strategy: Strategy to validate
            symbol: Trading symbol
            train_period_days: Training period length
            test_period_days: Testing period length

        Returns: Validation results
        """
        logger.info(f"📈 Walk-Forward Validation for {strategy.name}...")

        current_date = self.start_date
        validation_results = []

        while current_date < self.end_date:
            train_start = current_date
            train_end = current_date + timedelta(days=train_period_days)
            test_end = min(train_end + timedelta(days=test_period_days), self.end_date)

            if test_end > self.end_date:
                break

            logger.info(f"  Train: {train_start.date()} - {train_end.date()}, Test: {train_end.date()} - {test_end.date()}")

            # Backtest on training period
            train_result = self.backtest_strategy(strategy, symbol, train_start, train_end)
            train_metrics = train_result.calculate_metrics()

            # Backtest on testing period
            test_result = self.backtest_strategy(strategy, symbol, train_end, test_end)
            test_metrics = test_result.calculate_metrics()

            validation_results.append({
                'train_period': f"{train_start.date()} - {train_end.date()}",
                'test_period': f"{train_end.date()} - {test_end.date()}",
                'train_metrics': train_metrics,
                'test_metrics': test_metrics,
                'consistency': self._calculate_consistency(train_metrics, test_metrics)
            })

            current_date = test_end

        return {
            'strategy': strategy.name,
            'validation_results': validation_results,
            'average_consistency': np.mean([r['consistency'] for r in validation_results]) if validation_results else 0
        }

    def _calculate_consistency(self, train_metrics: Dict, test_metrics: Dict) -> float:
        """Calculate consistency between train and test metrics."""
        train_sharpe = train_metrics.get('sharpe_ratio', 0)
        test_sharpe = test_metrics.get('sharpe_ratio', 0)

        if train_sharpe == 0:
            return 0

        return min(test_sharpe / train_sharpe, 1.0)

    def compare_live_results(self, strategy_id: int) -> Dict:
        """Compare backtest results with live trading results.

        Args:
            strategy_id: Strategy ID in database

        Returns: Comparison metrics
        """
        logger.info(f"📊 Comparing live results for strategy {strategy_id}...")

        # Get live trades
        live_trades = self.db.fetch_df(
            "SELECT * FROM trades WHERE strategy_id = %s AND status = 'CLOSED' ORDER BY exit_time DESC LIMIT 100",
            (strategy_id,)
        )

        if len(live_trades) == 0:
            logger.warning("⚠️  No live trades found")
            return {}

        # Calculate live metrics
        live_win_rate = len(live_trades[live_trades['profit_loss'] > 0]) / len(live_trades) if len(live_trades) > 0 else 0
        live_profit = live_trades['profit_loss'].sum()

        return {
            'live_trades': len(live_trades),
            'live_win_rate': live_win_rate,
            'live_profit': live_profit,
            'live_avg_profit': live_trades['profit_loss'].mean(),
            'live_max_loss': live_trades['profit_loss'].min(),
            'timestamp': datetime.now()
        }


class BacktestReporter:
    """Generate backtest reports."""

    @staticmethod
    def generate_report(result: BacktestResult, strategy_name: str) -> str:
        """Generate text report.

        Args:
            result: BacktestResult object
            strategy_name: Strategy name

        Returns: Formatted report string
        """
        metrics = result.calculate_metrics()

        report = f"""
╔════════════════════════════════════════════════════════════╗
║         BACKTEST REPORT: {strategy_name:40} ║
╚════════════════════════════════════════════════════════════╝

📊 PERFORMANCE METRICS
─────────────────────────────────────────
Total Profit:          ${metrics['total_profit']:>20,.2f}
Return:                {metrics['return_pct']:>20.2f}%
Final Equity:          ${metrics['final_equity']:>20,.2f}

📈 TRADE STATISTICS
─────────────────────────────────────────
Total Trades:          {metrics['total_trades']:>20}
Winning Trades:        {metrics['winning_trades']:>20}
Losing Trades:         {metrics['losing_trades']:>20}
Win Rate:              {metrics['win_rate']:>20.1%}
Avg Profit/Trade:      ${metrics['avg_profit']:>20,.2f}
Avg Win:               ${metrics['avg_win']:>20,.2f}
Avg Loss:              ${metrics['avg_loss']:>20,.2f}
Profit Factor:         {metrics['profit_factor']:>20.2f}

📉 RISK METRICS
─────────────────────────────────────────
Max Drawdown:          {metrics['max_drawdown']:>20.2f}%

🎯 RISK-ADJUSTED RETURNS
─────────────────────────────────────────
Sharpe Ratio:          {metrics['sharpe_ratio']:>20.2f}
Sortino Ratio:         {metrics['sortino_ratio']:>20.2f}
Calmar Ratio:          {metrics['calmar_ratio']:>20.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return report

    @staticmethod
    def export_csv(result: BacktestResult, filename: str):
        """Export results to CSV.

        Args:
            result: BacktestResult object
            filename: Output filename
        """
        trades_df = pd.DataFrame(result.trades)
        equity_df = pd.DataFrame({
            'timestamp': result.timestamps,
            'equity': result.equity_curve
        })

        with open(filename, 'w') as f:
            f.write("=== TRADES ===\n")
            f.write(trades_df.to_csv())
            f.write("\n=== EQUITY CURVE ===\n")
            f.write(equity_df.to_csv())

        logger.info(f"✅ Report exported: {filename}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example usage
    backtester = Backtester(
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2024, 1, 1)
    )

    # Create test strategy
    strategy = RSIStrategy(
        name="RSI Test",
        symbol="XAUUSD",
        timeframe=60,
        config={'period': 14, 'overbought': 70, 'oversold': 30}
    )

    # Run backtest
    result = backtester.backtest_strategy(strategy, "XAUUSD")
    metrics = result.calculate_metrics()

    # Generate report
    report = BacktestReporter.generate_report(result, "RSI Strategy")
    print(report)
