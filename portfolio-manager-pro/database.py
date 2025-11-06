"""PostgreSQL Database Module - Portfolio Manager Pro."""
import psycopg2
from psycopg2 import sql
import pandas as pd
from datetime import datetime
import logging
from config import settings

logger = logging.getLogger(__name__)


class Database:
    """PostgreSQL database operations."""

    def __init__(self):
        """Initialize database connection."""
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Connect to PostgreSQL."""
        try:
            self.conn = psycopg2.connect(settings.DATABASE_URL)
            self.cursor = self.conn.cursor()
            logger.info(f"✅ Connected to PostgreSQL ({settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME})")
        except psycopg2.Error as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise

    def close(self):
        """Close connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            logger.info("✅ Database connection closed")

    def execute(self, query, params=None, fetch=False):
        """Execute query."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            self.conn.commit()

            if fetch:
                return self.cursor.fetchall()

            return self.cursor

        except psycopg2.Error as e:
            self.conn.rollback()
            logger.error(f"❌ Query execution failed: {e}")
            raise

    def fetch_one(self, query, params=None):
        """Fetch single row."""
        self.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        """Fetch all rows."""
        self.execute(query, params)
        return self.cursor.fetchall()

    def fetch_df(self, query, params=None):
        """Fetch as DataFrame."""
        self.execute(query, params)
        columns = [desc[0] for desc in self.cursor.description]
        data = self.cursor.fetchall()
        return pd.DataFrame(data, columns=columns) if data else pd.DataFrame()

    # ========== STRATEGIES ==========

    def register_strategy(self, name: str, strategy_type: str, config: dict, enabled: bool = True):
        """Register new strategy."""
        query = """
            INSERT INTO strategies (name, type, config, enabled, created_at, updated_at)
            VALUES (%s, %s, %s::jsonb, %s, NOW(), NOW())
            RETURNING id
        """
        import json
        result = self.fetch_one(query, (name, strategy_type, json.dumps(config), enabled))
        strategy_id = result[0] if result else None

        logger.info(f"✅ Strategy registered: {name} (ID: {strategy_id})")
        return strategy_id

    def get_active_strategies(self):
        """Get all active strategies."""
        query = "SELECT id, name, type, config FROM strategies WHERE enabled = TRUE ORDER BY created_at"
        return self.fetch_df(query)

    def update_strategy_allocation(self, strategy_id: int, allocation: float):
        """Update strategy allocation (%)."""
        query = "UPDATE strategies SET allocation = %s, updated_at = NOW() WHERE id = %s"
        self.execute(query, (allocation, strategy_id))
        logger.info(f"✅ Strategy {strategy_id} allocation set to {allocation}%")

    def update_strategy_performance(self, strategy_id: int, performance_score: float):
        """Update strategy performance score."""
        query = "UPDATE strategies SET performance_score = %s, updated_at = NOW() WHERE id = %s"
        self.execute(query, (performance_score, strategy_id))

    def disable_strategy(self, strategy_id: int):
        """Disable strategy."""
        query = "UPDATE strategies SET enabled = FALSE, updated_at = NOW() WHERE id = %s"
        self.execute(query, (strategy_id,))
        logger.info(f"✅ Strategy {strategy_id} disabled")

    # ========== MARKET DATA ==========

    def insert_candle(self, symbol: str, timeframe: int, ohlcv: dict):
        """Insert market candle."""
        query = """
            INSERT INTO market_data
            (symbol, timeframe, timestamp, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol, timeframe, timestamp) DO NOTHING
        """
        params = (
            symbol,
            timeframe,
            datetime.fromtimestamp(ohlcv['time']),
            ohlcv['open'],
            ohlcv['high'],
            ohlcv['low'],
            ohlcv['close'],
            ohlcv['volume']
        )
        self.execute(query, params)

    def get_candles(self, symbol: str, timeframe: int, limit: int = 500):
        """Get last N candles."""
        query = """
            SELECT timestamp, open, high, low, close, volume
            FROM market_data
            WHERE symbol = %s AND timeframe = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """
        df = self.fetch_df(query, (symbol, timeframe, limit))
        return df.iloc[::-1] if len(df) > 0 else df

    # ========== SIGNALS ==========

    def insert_signal(self, strategy_id: int, symbol: str, signal: str, confidence: float, details: dict = None):
        """Insert strategy signal."""
        query = """
            INSERT INTO strategy_signals
            (strategy_id, timestamp, symbol, signal, confidence, details)
            VALUES (%s, NOW(), %s, %s, %s, %s::jsonb)
        """
        import json
        self.execute(query, (strategy_id, symbol, signal, confidence, json.dumps(details or {})))

    def get_latest_signals(self, limit: int = 100):
        """Get latest signals from all strategies."""
        query = """
            SELECT s.id, st.name, s.symbol, s.signal, s.confidence, s.timestamp
            FROM strategy_signals s
            JOIN strategies st ON s.strategy_id = st.id
            ORDER BY s.timestamp DESC
            LIMIT %s
        """
        return self.fetch_df(query, (limit,))

    # ========== TRADES ==========

    def insert_trade(self, strategy_id: int, symbol: str, direction: str, entry_price: float, lot_size: float):
        """Insert new trade."""
        query = """
            INSERT INTO trades
            (strategy_id, symbol, direction, entry_price, entry_time, lot_size, status)
            VALUES (%s, %s, %s, %s, NOW(), %s, 'OPEN')
            RETURNING id
        """
        result = self.fetch_one(query, (strategy_id, symbol, direction, entry_price, lot_size))
        trade_id = result[0] if result else None

        logger.info(f"✅ Trade opened: {direction} {lot_size} {symbol} @ {entry_price}")
        return trade_id

    def close_trade(self, trade_id: int, exit_price: float):
        """Close trade."""
        query = """
            UPDATE trades
            SET exit_price = %s,
                exit_time = NOW(),
                profit_loss = (exit_price - entry_price) * lot_size,
                profit_pct = ((exit_price - entry_price) / entry_price * 100),
                status = 'CLOSED'
            WHERE id = %s
        """
        self.execute(query, (exit_price, trade_id))
        logger.info(f"✅ Trade {trade_id} closed @ {exit_price}")

    def get_open_trades(self, strategy_id: int = None):
        """Get all open trades."""
        if strategy_id:
            query = "SELECT * FROM trades WHERE status = 'OPEN' AND strategy_id = %s"
            return self.fetch_df(query, (strategy_id,))
        else:
            return self.fetch_df("SELECT * FROM trades WHERE status = 'OPEN'")

    def get_daily_trades(self, date=None):
        """Get trades for specific date."""
        if not date:
            date = datetime.now().date()

        query = """
            SELECT * FROM trades
            WHERE DATE(entry_time) = %s
            ORDER BY entry_time DESC
        """
        return self.fetch_df(query, (date,))

    # ========== POSITIONS ==========

    def insert_position(self, strategy_id: int, symbol: str, direction: str, lot_size: float, entry_price: float):
        """Insert open position."""
        query = """
            INSERT INTO positions
            (strategy_id, symbol, direction, lot_size, entry_price, current_price, open_time)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            RETURNING id
        """
        result = self.fetch_one(query, (strategy_id, symbol, direction, lot_size, entry_price, entry_price))
        return result[0] if result else None

    def get_all_positions(self):
        """Get all open positions."""
        query = "SELECT id, strategy_id, symbol, direction, lot_size, entry_price, current_price FROM positions"
        return self.fetch_df(query)

    def update_position_price(self, position_id: int, current_price: float):
        """Update position current price."""
        query = """
            UPDATE positions
            SET current_price = %s,
                profit_loss = (current_price - entry_price) * lot_size
            WHERE id = %s
        """
        self.execute(query, (current_price, position_id))

    # ========== PORTFOLIO METRICS ==========

    def insert_daily_metrics(self, metrics: dict):
        """Insert daily portfolio metrics."""
        query = """
            INSERT INTO portfolio_metrics
            (date, total_balance, equity, drawdown_pct, daily_pl, win_rate, sharpe_ratio, correlation_matrix)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb)
            ON CONFLICT (date) DO UPDATE SET
                total_balance = EXCLUDED.total_balance,
                equity = EXCLUDED.equity,
                drawdown_pct = EXCLUDED.drawdown_pct,
                daily_pl = EXCLUDED.daily_pl,
                win_rate = EXCLUDED.win_rate,
                sharpe_ratio = EXCLUDED.sharpe_ratio,
                correlation_matrix = EXCLUDED.correlation_matrix
        """
        import json
        params = (
            metrics.get('date', datetime.now().date()),
            metrics.get('total_balance'),
            metrics.get('equity'),
            metrics.get('drawdown_pct'),
            metrics.get('daily_pl'),
            metrics.get('win_rate'),
            metrics.get('sharpe_ratio'),
            json.dumps(metrics.get('correlation_matrix', {}))
        )
        self.execute(query, params)
        logger.info(f"✅ Portfolio metrics recorded for {metrics.get('date')}")

    def get_portfolio_history(self, days: int = 30):
        """Get portfolio metrics history."""
        query = """
            SELECT date, total_balance, equity, drawdown_pct, daily_pl, win_rate, sharpe_ratio
            FROM portfolio_metrics
            WHERE date >= NOW() - INTERVAL '%s days'
            ORDER BY date DESC
        """
        return self.fetch_df(query, (days,))

    # ========== RL TRAINING ==========

    def log_rl_training(self, episode: int, reward: float, total_profit: float, model_version: str = "v1"):
        """Log RL training metrics."""
        query = """
            INSERT INTO rl_models (episode, reward, total_profit, model_version, created_at, is_active)
            VALUES (%s, %s, %s, %s, NOW(), FALSE)
        """
        self.execute(query, (episode, reward, total_profit, model_version))

    def get_rl_history(self, limit: int = 100):
        """Get RL training history."""
        query = "SELECT * FROM rl_models ORDER BY episode DESC LIMIT %s"
        return self.fetch_df(query, (limit,))

    # ========== AUDIT LOGS ==========

    def log_event(self, event_type: str, actor: str, details: dict, status: str = "SUCCESS"):
        """Log audit event."""
        query = """
            INSERT INTO audit_logs (timestamp, event_type, actor, details, status)
            VALUES (NOW(), %s, %s, %s::jsonb, %s)
        """
        import json
        self.execute(query, (event_type, actor, json.dumps(details), status))


# ========== DATABASE SCHEMA CREATION ==========

DATABASE_SCHEMA = """
-- Strategies
CREATE TABLE IF NOT EXISTS strategies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,
    config JSONB,
    enabled BOOLEAN DEFAULT TRUE,
    allocation DECIMAL(5, 2) DEFAULT 0,
    performance_score DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Market Data
CREATE TABLE IF NOT EXISTS market_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    timeframe INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    open DECIMAL(20, 8),
    high DECIMAL(20, 8),
    low DECIMAL(20, 8),
    close DECIMAL(20, 8),
    volume INTEGER,
    CONSTRAINT unique_candle UNIQUE (symbol, timeframe, timestamp)
);
CREATE INDEX IF NOT EXISTS idx_market_data ON market_data(symbol, timeframe, timestamp DESC);

-- Strategy Signals
CREATE TABLE IF NOT EXISTS strategy_signals (
    id SERIAL PRIMARY KEY,
    strategy_id INTEGER REFERENCES strategies(id),
    timestamp TIMESTAMP DEFAULT NOW(),
    symbol VARCHAR(20),
    signal VARCHAR(20),
    confidence DECIMAL(3, 2),
    details JSONB
);

-- Trades
CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    strategy_id INTEGER REFERENCES strategies(id),
    symbol VARCHAR(20),
    direction VARCHAR(10),
    entry_price DECIMAL(20, 8),
    exit_price DECIMAL(20, 8),
    lot_size DECIMAL(20, 8),
    profit_loss DECIMAL(20, 8),
    profit_pct DECIMAL(10, 2),
    entry_time TIMESTAMP,
    exit_time TIMESTAMP,
    status VARCHAR(20) DEFAULT 'OPEN',
    INDEX (strategy_id, entry_time)
);

-- Positions
CREATE TABLE IF NOT EXISTS positions (
    id SERIAL PRIMARY KEY,
    strategy_id INTEGER REFERENCES strategies(id),
    symbol VARCHAR(20),
    direction VARCHAR(10),
    lot_size DECIMAL(20, 8),
    entry_price DECIMAL(20, 8),
    current_price DECIMAL(20, 8),
    profit_loss DECIMAL(20, 8),
    open_time TIMESTAMP
);

-- Portfolio Metrics
CREATE TABLE IF NOT EXISTS portfolio_metrics (
    id SERIAL PRIMARY KEY,
    date DATE UNIQUE,
    total_balance DECIMAL(20, 8),
    equity DECIMAL(20, 8),
    drawdown_pct DECIMAL(5, 2),
    daily_pl DECIMAL(20, 8),
    win_rate DECIMAL(5, 2),
    sharpe_ratio DECIMAL(10, 4),
    correlation_matrix JSONB
);

-- RL Models
CREATE TABLE IF NOT EXISTS rl_models (
    id SERIAL PRIMARY KEY,
    episode INTEGER,
    reward DECIMAL(20, 8),
    total_profit DECIMAL(20, 8),
    model_version VARCHAR(50),
    created_at TIMESTAMP,
    is_active BOOLEAN DEFAULT FALSE
);

-- Audit Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    event_type VARCHAR(50),
    actor VARCHAR(50),
    details JSONB,
    status VARCHAR(20)
);
"""


def initialize_database():
    """Initialize database schema."""
    try:
        db = Database()
        db.execute(DATABASE_SCHEMA)
        logger.info("✅ Database schema initialized")
        db.close()
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    initialize_database()
