"""Portfolio Manager Pro - Configuration Management."""
import os
from dotenv import load_dotenv
from pydantic import BaseSettings
from pathlib import Path

load_dotenv()


class Settings(BaseSettings):
    """Global configuration for Portfolio Manager Pro."""

    # ========== DATABASE ==========
    DB_HOST: str = os.getenv("DB_HOST", "51.77.58.92")
    DB_PORT: int = int(os.getenv("DB_PORT", 1993))
    DB_USER: str = os.getenv("DB_USER", "pawwasfx")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "bazadanych")

    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # ========== MT5 - LOCAL ==========
    MT5_ACCOUNT_LOCAL: str = os.getenv("MT5_ACCOUNT_LOCAL", "")
    MT5_PASSWORD_LOCAL: str = os.getenv("MT5_PASSWORD_LOCAL", "")
    MT5_SERVER_LOCAL: str = os.getenv("MT5_SERVER_LOCAL", "")
    MT5_PATH_LOCAL: str = os.getenv("MT5_PATH_LOCAL", "C:\\Program Files\\MetaTrader 5")

    # ========== MT5 - REMOTE (on VPS/Server) ==========
    MT5_REMOTE_ENABLED: bool = os.getenv("MT5_REMOTE_ENABLED", "false").lower() == "true"
    MT5_REMOTE_HOST: str = os.getenv("MT5_REMOTE_HOST", "")
    MT5_REMOTE_PORT: int = int(os.getenv("MT5_REMOTE_PORT", 22))
    MT5_REMOTE_USER: str = os.getenv("MT5_REMOTE_USER", "")
    MT5_REMOTE_PASSWORD: str = os.getenv("MT5_REMOTE_PASSWORD", "")
    MT5_REMOTE_SSH_KEY: str = os.getenv("MT5_REMOTE_SSH_KEY", "")
    MT5_REMOTE_PATH: str = os.getenv("MT5_REMOTE_PATH", "/home/user/mt5")
    MT5_REMOTE_PROTOCOL: str = os.getenv("MT5_REMOTE_PROTOCOL", "ssh")  # ssh, rdp

    # ========== TRADING SYMBOLS & TIMEFRAMES ==========
    SYMBOLS: list = ["XAUUSD", "NASDAQ"]
    TIMEFRAMES: dict = {
        1: "M1",
        5: "M5",
        15: "M15",
        60: "H1",
        240: "H4",
        1440: "D1"
    }

    # ========== PORTFOLIO SETTINGS ==========
    INITIAL_CAPITAL: float = float(os.getenv("INITIAL_CAPITAL", 100000))
    MAX_STRATEGIES: int = int(os.getenv("MAX_STRATEGIES", 50))
    DEFAULT_TIMEFRAME: int = int(os.getenv("DEFAULT_TIMEFRAME", 60))  # 1H

    # ========== RISK MANAGEMENT ==========
    MAX_DAILY_LOSS_PCT: float = float(os.getenv("MAX_DAILY_LOSS_PCT", 5))
    DRAWDOWN_SAFE: float = float(os.getenv("DRAWDOWN_SAFE", 4))
    DRAWDOWN_CAUTION: float = float(os.getenv("DRAWDOWN_CAUTION", 8))
    DRAWDOWN_CRITICAL: float = float(os.getenv("DRAWDOWN_CRITICAL", 12))

    MAX_CORRELATION: float = float(os.getenv("MAX_CORRELATION", 0.8))
    MAX_POSITION_PCT: float = float(os.getenv("MAX_POSITION_PCT", 5))  # 5% per position
    MAX_SECTOR_PCT: float = float(os.getenv("MAX_SECTOR_PCT", 20))  # 20% per sector

    POSITION_SIZING: str = os.getenv("POSITION_SIZING", "kelly")  # kelly, fixed, adaptive
    FIXED_LOT_SIZE: float = float(os.getenv("FIXED_LOT_SIZE", 1.0))
    KELLY_FRACTION: float = float(os.getenv("KELLY_FRACTION", 0.25))  # 25% Kelly

    # ========== RL CONFIGURATION ==========
    RL_ENABLED: bool = os.getenv("RL_ENABLED", "true").lower() == "true"
    RL_MODEL_TYPE: str = os.getenv("RL_MODEL_TYPE", "PPO")  # DQN, PPO, A2C
    RL_LEARNING_RATE: float = float(os.getenv("RL_LEARNING_RATE", 0.0001))  # Lower for stable convergence
    RL_BUFFER_SIZE: int = int(os.getenv("RL_BUFFER_SIZE", 100000))
    RL_BATCH_SIZE: int = int(os.getenv("RL_BATCH_SIZE", 128))  # Increased
    RL_GAMMA: float = float(os.getenv("RL_GAMMA", 0.97))  # Prioritize recent rewards
    RL_TAU: float = float(os.getenv("RL_TAU", 0.005))

    RL_TRAINING_FREQUENCY: str = os.getenv("RL_TRAINING_FREQUENCY", "daily")  # hourly, daily, weekly
    RL_RETRAINING_TRIGGER: str = os.getenv("RL_RETRAINING_TRIGGER", "performance")  # fixed, performance
    RL_MODEL_PATH: str = os.getenv("RL_MODEL_PATH", "./models/")
    RL_TOTAL_TIMESTEPS: int = int(os.getenv("RL_TOTAL_TIMESTEPS", 1000000))

    # ========== BACKTESTING ==========
    BACKTEST_PARALLEL: bool = os.getenv("BACKTEST_PARALLEL", "true").lower() == "true"
    BACKTEST_WORKERS: int = int(os.getenv("BACKTEST_WORKERS", 4))
    BACKTEST_COMMISSION: float = float(os.getenv("BACKTEST_COMMISSION", 0.0001))  # 0.01%

    # ========== MONITORING & ALERTS ==========
    TELEGRAM_ENABLED: bool = os.getenv("TELEGRAM_ENABLED", "false").lower() == "true"
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

    EMAIL_ENABLED: bool = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "")
    EMAIL_SMTP_SERVER: str = os.getenv("EMAIL_SMTP_SERVER", "")
    EMAIL_SMTP_PORT: int = int(os.getenv("EMAIL_SMTP_PORT", 587))
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")

    # ========== LOGGING ==========
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "./logs/portfolio_manager.log")
    LOG_STRUCTURED: bool = os.getenv("LOG_STRUCTURED", "true").lower() == "true"

    LOG_DIR = Path(LOG_FILE).parent
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # ========== ENVIRONMENT ==========
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "demo")  # demo, paper, live
    IS_DEMO: bool = ENVIRONMENT == "demo"
    IS_PAPER: bool = ENVIRONMENT == "paper"
    IS_LIVE: bool = ENVIRONMENT == "live"

    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @classmethod
    def validate_config(cls):
        """Validate critical configuration."""
        errors = []

        # Database validation
        if not cls.DB_PASSWORD:
            errors.append("❌ DB_PASSWORD not configured")

        # MT5 validation
        if cls.MT5_REMOTE_ENABLED:
            if not cls.MT5_REMOTE_HOST:
                errors.append("❌ MT5_REMOTE_HOST not set but MT5_REMOTE_ENABLED=true")
            if not cls.MT5_REMOTE_USER:
                errors.append("❌ MT5_REMOTE_USER not set but MT5_REMOTE_ENABLED=true")
            if not (cls.MT5_REMOTE_PASSWORD or cls.MT5_REMOTE_SSH_KEY):
                errors.append("❌ Neither MT5_REMOTE_PASSWORD nor MT5_REMOTE_SSH_KEY provided")

        # RL validation
        if cls.RL_ENABLED and cls.RL_MODEL_TYPE not in ["DQN", "PPO", "A2C"]:
            errors.append(f"❌ Unknown RL_MODEL_TYPE: {cls.RL_MODEL_TYPE}")

        # Risk validation
        if cls.MAX_DAILY_LOSS_PCT <= 0 or cls.MAX_DAILY_LOSS_PCT > 50:
            errors.append(f"❌ MAX_DAILY_LOSS_PCT must be between 0-50%, got {cls.MAX_DAILY_LOSS_PCT}")

        if errors:
            raise ValueError("Configuration validation errors:\n" + "\n".join(errors))

        return True

    @classmethod
    def display(cls):
        """Display current configuration."""
        print("\n" + "="*70)
        print("🤖 PORTFOLIO MANAGER PRO - Configuration")
        print("="*70)

        print("\n📊 DATABASE:")
        print(f"  Host: {cls.DB_HOST}:{cls.DB_PORT}")
        print(f"  Database: {cls.DB_NAME}")

        print("\n📈 MT5 CONFIGURATION:")
        if cls.MT5_REMOTE_ENABLED:
            print(f"  Mode: REMOTE (VPS/Server)")
            print(f"  Host: {cls.MT5_REMOTE_HOST}:{cls.MT5_REMOTE_PORT}")
            print(f"  User: {cls.MT5_REMOTE_USER}")
            print(f"  Path: {cls.MT5_REMOTE_PATH}")
            print(f"  Protocol: {cls.MT5_REMOTE_PROTOCOL}")
        else:
            print(f"  Mode: LOCAL")
            print(f"  Path: {cls.MT5_PATH_LOCAL}")

        print("\n💼 PORTFOLIO:")
        print(f"  Capital: ${cls.INITIAL_CAPITAL:,.0f}")
        print(f"  Max Strategies: {cls.MAX_STRATEGIES}")
        print(f"  Position Sizing: {cls.POSITION_SIZING}")

        print("\n🛡️  RISK MANAGEMENT:")
        print(f"  Max Daily Loss: {cls.MAX_DAILY_LOSS_PCT}%")
        print(f"  Drawdown Limits: Safe={cls.DRAWDOWN_SAFE}%, Caution={cls.DRAWDOWN_CAUTION}%, Critical={cls.DRAWDOWN_CRITICAL}%")
        print(f"  Max Position: {cls.MAX_POSITION_PCT}%")
        print(f"  Max Correlation: {cls.MAX_CORRELATION}")

        print("\n🧠 AI/RL:")
        print(f"  RL Enabled: {cls.RL_ENABLED}")
        if cls.RL_ENABLED:
            print(f"  Model: {cls.RL_MODEL_TYPE}")
            print(f"  Training Frequency: {cls.RL_TRAINING_FREQUENCY}")
            print(f"  Learning Rate: {cls.RL_LEARNING_RATE}")

        print("\n📊 ALERTS:")
        print(f"  Telegram: {cls.TELEGRAM_ENABLED}")
        print(f"  Email: {cls.EMAIL_ENABLED}")

        print("\n⚙️  ENVIRONMENT:")
        print(f"  Mode: {cls.ENVIRONMENT.upper()}")
        print(f"  Debug: {cls.DEBUG}")
        print(f"  Log Level: {cls.LOG_LEVEL}")

        print("="*70 + "\n")


# Initialize settings
settings = Settings()

if __name__ == "__main__":
    settings.display()
