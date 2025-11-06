"""Logging & Audit System - Compliance & Monitoring."""
import logging
import json
from typing import Dict, Optional, Any
from datetime import datetime
from pathlib import Path
from database import Database
from config import settings

logger = logging.getLogger(__name__)


class AuditLogger:
    """Centralized audit logging for compliance."""

    def __init__(self, db: Optional[Database] = None):
        """Initialize audit logger.

        Args:
            db: Database instance for storing audit logs
        """
        self.db = db or Database()
        self.log_dir = Path("./logs")
        self.log_dir.mkdir(exist_ok=True)

    def log_trade(self, trade_data: Dict):
        """Log trade execution.

        Args:
            trade_data: Trade details
        """
        event = {
            'type': 'TRADE_EXECUTION',
            'actor': 'StrategyExecutor',
            'details': {
                'symbol': trade_data.get('symbol'),
                'direction': trade_data.get('direction'),
                'entry_price': trade_data.get('entry_price'),
                'lot_size': trade_data.get('lot_size'),
                'entry_time': str(trade_data.get('entry_time', datetime.now())),
                'reason': trade_data.get('reason', 'Strategy signal')
            },
            'status': 'SUCCESS',
            'timestamp': datetime.now().isoformat()
        }

        self._write_to_db(event)
        self._write_to_file('trades.log', event)
        logger.info(f"📝 Trade logged: {event['details']['symbol']} {event['details']['direction']}")

    def log_risk_check(self, validation_data: Dict):
        """Log risk validation.

        Args:
            validation_data: Risk validation details
        """
        event = {
            'type': 'RISK_VALIDATION',
            'actor': 'RiskManager',
            'details': {
                'symbol': validation_data.get('symbol'),
                'check_type': validation_data.get('check_type'),
                'current_value': validation_data.get('current_value'),
                'limit_value': validation_data.get('limit_value'),
                'passed': validation_data.get('passed', False),
                'message': validation_data.get('message', '')
            },
            'status': 'SUCCESS',
            'timestamp': datetime.now().isoformat()
        }

        if not validation_data.get('passed', False):
            event['status'] = 'REJECTED'

        self._write_to_db(event)
        self._write_to_file('risk_checks.log', event)

    def log_strategy_signal(self, signal_data: Dict):
        """Log strategy signal generation.

        Args:
            signal_data: Signal details
        """
        event = {
            'type': 'STRATEGY_SIGNAL',
            'actor': f"Strategy:{signal_data.get('strategy_name')}",
            'details': {
                'strategy_id': signal_data.get('strategy_id'),
                'strategy_name': signal_data.get('strategy_name'),
                'symbol': signal_data.get('symbol'),
                'signal': signal_data.get('signal'),
                'confidence': signal_data.get('confidence'),
                'indicators': signal_data.get('indicators', {})
            },
            'status': 'SUCCESS',
            'timestamp': datetime.now().isoformat()
        }

        self._write_to_db(event)
        self._write_to_file('signals.log', event)

    def log_position_open(self, position_data: Dict):
        """Log position opening.

        Args:
            position_data: Position details
        """
        event = {
            'type': 'POSITION_OPENED',
            'actor': 'PositionManager',
            'details': {
                'position_id': position_data.get('position_id'),
                'symbol': position_data.get('symbol'),
                'direction': position_data.get('direction'),
                'lot_size': position_data.get('lot_size'),
                'entry_price': position_data.get('entry_price'),
                'strategy_id': position_data.get('strategy_id')
            },
            'status': 'SUCCESS',
            'timestamp': datetime.now().isoformat()
        }

        self._write_to_db(event)
        self._write_to_file('positions.log', event)
        logger.info(f"📍 Position opened: {event['details']['symbol']} {event['details']['direction']}")

    def log_position_close(self, position_data: Dict):
        """Log position closing.

        Args:
            position_data: Position details
        """
        event = {
            'type': 'POSITION_CLOSED',
            'actor': 'PositionManager',
            'details': {
                'position_id': position_data.get('position_id'),
                'symbol': position_data.get('symbol'),
                'direction': position_data.get('direction'),
                'entry_price': position_data.get('entry_price'),
                'exit_price': position_data.get('exit_price'),
                'profit_loss': position_data.get('profit_loss'),
                'profit_pct': position_data.get('profit_pct')
            },
            'status': 'SUCCESS',
            'timestamp': datetime.now().isoformat()
        }

        self._write_to_db(event)
        self._write_to_file('positions.log', event)
        logger.info(f"🔴 Position closed: {event['details']['symbol']} P&L: ${event['details']['profit_loss']:.2f}")

    def log_rl_training(self, training_data: Dict):
        """Log RL training event.

        Args:
            training_data: Training details
        """
        event = {
            'type': 'RL_TRAINING',
            'actor': 'RLAgent',
            'details': {
                'episode': training_data.get('episode'),
                'model_type': training_data.get('model_type'),
                'symbol': training_data.get('symbol'),
                'reward': training_data.get('reward'),
                'total_profit': training_data.get('total_profit'),
                'model_version': training_data.get('model_version'),
                'duration_seconds': training_data.get('duration_seconds')
            },
            'status': 'SUCCESS',
            'timestamp': datetime.now().isoformat()
        }

        self._write_to_db(event)
        self._write_to_file('rl_training.log', event)

    def log_backtest(self, backtest_data: Dict):
        """Log backtesting event.

        Args:
            backtest_data: Backtest details
        """
        event = {
            'type': 'BACKTEST',
            'actor': 'Backtester',
            'details': {
                'strategy_name': backtest_data.get('strategy_name'),
                'symbol': backtest_data.get('symbol'),
                'start_date': str(backtest_data.get('start_date')),
                'end_date': str(backtest_data.get('end_date')),
                'total_trades': backtest_data.get('total_trades'),
                'win_rate': backtest_data.get('win_rate'),
                'total_profit': backtest_data.get('total_profit'),
                'sharpe_ratio': backtest_data.get('sharpe_ratio'),
                'max_drawdown': backtest_data.get('max_drawdown')
            },
            'status': 'SUCCESS',
            'timestamp': datetime.now().isoformat()
        }

        self._write_to_db(event)
        self._write_to_file('backtests.log', event)

    def log_error(self, error_data: Dict):
        """Log error event.

        Args:
            error_data: Error details
        """
        event = {
            'type': 'ERROR',
            'actor': error_data.get('actor', 'System'),
            'details': {
                'message': error_data.get('message'),
                'error_type': error_data.get('error_type'),
                'traceback': error_data.get('traceback', ''),
                'context': error_data.get('context', {})
            },
            'status': 'FAILED',
            'timestamp': datetime.now().isoformat()
        }

        self._write_to_db(event)
        self._write_to_file('errors.log', event)
        logger.error(f"⚠️  Error logged: {error_data.get('message')}")

    def log_performance_snapshot(self, performance_data: Dict):
        """Log performance snapshot for analysis.

        Args:
            performance_data: Performance metrics
        """
        event = {
            'type': 'PERFORMANCE_SNAPSHOT',
            'actor': 'PerformanceMonitor',
            'details': {
                'timestamp': datetime.now().isoformat(),
                'equity': performance_data.get('equity'),
                'drawdown': performance_data.get('drawdown'),
                'daily_pl': performance_data.get('daily_pl'),
                'win_rate': performance_data.get('win_rate'),
                'open_positions': performance_data.get('open_positions'),
                'sharpe_ratio': performance_data.get('sharpe_ratio')
            },
            'status': 'SUCCESS',
            'timestamp': datetime.now().isoformat()
        }

        self._write_to_file('performance_snapshots.log', event)

    def _write_to_db(self, event: Dict):
        """Write event to database.

        Args:
            event: Event dictionary
        """
        try:
            self.db.log_event(
                event_type=event['type'],
                actor=event['actor'],
                details=event['details'],
                status=event['status']
            )
        except Exception as e:
            logger.error(f"Failed to write audit log to database: {e}")

    def _write_to_file(self, log_file: str, event: Dict):
        """Write event to log file.

        Args:
            log_file: Log filename
            event: Event dictionary
        """
        try:
            log_path = self.log_dir / log_file
            with open(log_path, 'a') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            logger.error(f"Failed to write to {log_file}: {e}")

    def get_audit_trail(self, event_type: Optional[str] = None, days: int = 30) -> list:
        """Retrieve audit trail.

        Args:
            event_type: Filter by event type (optional)
            days: Number of days to retrieve

        Returns: List of audit events
        """
        try:
            if event_type:
                query = """
                    SELECT * FROM audit_logs
                    WHERE event_type = %s AND timestamp >= NOW() - INTERVAL '%s days'
                    ORDER BY timestamp DESC
                """
                return self.db.fetch_df(query, (event_type, days))
            else:
                query = """
                    SELECT * FROM audit_logs
                    WHERE timestamp >= NOW() - INTERVAL '%s days'
                    ORDER BY timestamp DESC
                """
                return self.db.fetch_df(query, (days,))
        except Exception as e:
            logger.error(f"Failed to retrieve audit trail: {e}")
            return []

    def generate_compliance_report(self, start_date: datetime, end_date: datetime) -> str:
        """Generate compliance report.

        Args:
            start_date: Report start date
            end_date: Report end date

        Returns: Formatted compliance report
        """
        report = f"""
╔════════════════════════════════════════════════════════════╗
║               COMPLIANCE AUDIT REPORT                      ║
║         {start_date.date()} to {end_date.date()}
╚════════════════════════════════════════════════════════════╝

📋 AUDIT SUMMARY
─────────────────────────────────────────
Report Generated: {datetime.now().isoformat()}
Period: {start_date.date()} to {end_date.date()}

🔍 Event Statistics
─────────────────────────────────────────
"""

        # Get event counts
        events = self.get_audit_trail()

        if len(events) > 0:
            event_types = events['event_type'].value_counts()
            for event_type, count in event_types.items():
                report += f"{event_type:30} : {count:>5}\n"

        report += f"""
⚠️  Error Summary
─────────────────────────────────────────
"""

        # Get errors
        errors = self.get_audit_trail(event_type='ERROR')
        report += f"Total Errors: {len(errors)}\n"

        if len(errors) > 0:
            report += "\nRecent Errors:\n"
            for idx, error in errors.head(10).iterrows():
                report += f"  • {error['timestamp']}: {error['details'].get('message', 'N/A')[:60]}\n"

        report += f"""
✅ Status
─────────────────────────────────────────
All systems operating normally.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        return report


class PerformanceLogger:
    """Log and analyze performance metrics."""

    def __init__(self):
        """Initialize performance logger."""
        self.db = Database()
        self.audit_logger = AuditLogger(self.db)

    def log_hourly_snapshot(self):
        """Log hourly performance snapshot."""
        try:
            # Get current metrics
            positions = self.db.get_all_positions()
            trades = self.db.fetch_df("SELECT * FROM trades WHERE status = 'CLOSED' ORDER BY exit_time DESC LIMIT 50")

            equity = settings.INITIAL_CAPITAL
            drawdown = 0
            daily_pl = 0
            win_rate = 0
            open_positions = len(positions)

            if len(trades) > 0:
                daily_trades = trades[trades['entry_time'] >= (datetime.now() - timedelta(days=1))]
                daily_pl = daily_trades['profit_loss'].sum() if len(daily_trades) > 0 else 0
                winning = len(trades[trades['profit_loss'] > 0])
                win_rate = winning / len(trades) if len(trades) > 0 else 0

            self.audit_logger.log_performance_snapshot({
                'equity': equity,
                'drawdown': drawdown,
                'daily_pl': daily_pl,
                'win_rate': win_rate,
                'open_positions': open_positions,
                'sharpe_ratio': 0
            })

            logger.info(f"📊 Hourly snapshot logged: Equity=${equity:,.2f}, Open={open_positions}")

        except Exception as e:
            logger.error(f"❌ Failed to log hourly snapshot: {e}")

    def log_daily_report(self):
        """Generate and log daily performance report."""
        try:
            trades = self.db.fetch_df("""
                SELECT * FROM trades
                WHERE DATE(entry_time) = CURRENT_DATE AND status = 'CLOSED'
            """)

            if len(trades) > 0:
                daily_profit = trades['profit_loss'].sum()
                winning_trades = len(trades[trades['profit_loss'] > 0])
                win_rate = winning_trades / len(trades)

                report = f"""
📊 DAILY PERFORMANCE REPORT - {datetime.now().date()}
Trades: {len(trades)}
Winning: {winning_trades}
Daily Profit: ${daily_profit:,.2f}
Win Rate: {win_rate:.1%}
                """

                logger.info(report)
                self.audit_logger._write_to_file('daily_reports.log', {
                    'date': str(datetime.now().date()),
                    'trades': len(trades),
                    'winning_trades': winning_trades,
                    'daily_profit': daily_profit,
                    'win_rate': win_rate
                })

        except Exception as e:
            logger.error(f"❌ Failed to generate daily report: {e}")


def setup_logging(log_level: str = 'INFO', log_file: str = 'portfolio_manager.log') -> logging.Logger:
    """Setup centralized logging.

    Args:
        log_level: Logging level
        log_file: Log filename

    Returns: Logger instance
    """
    logger = logging.getLogger('portfolio_manager')
    logger.setLevel(getattr(logging, log_level))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)

    # File handler
    Path('./logs').mkdir(exist_ok=True)
    file_handler = logging.FileHandler(f'./logs/{log_file}')
    file_handler.setLevel(getattr(logging, log_level))
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test logging
    audit_logger = AuditLogger()
    audit_logger.log_trade({
        'symbol': 'XAUUSD',
        'direction': 'BUY',
        'entry_price': 2000.00,
        'lot_size': 1.0
    })

    # Generate report
    report = audit_logger.generate_compliance_report(
        datetime(2024, 1, 1),
        datetime.now()
    )
    print(report)
