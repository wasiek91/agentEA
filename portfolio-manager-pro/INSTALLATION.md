# 🚀 Portfolio Manager Pro - Installation & Deployment Guide

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL 13+
- MetaTrader5 (local installation or VPS with MT5)
- Git

## 🔧 Installation Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/portfolio-manager-pro.git
cd portfolio-manager-pro
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

**Required Configuration in `.env`:**

```env
# DATABASE (Already pre-configured)
DB_HOST=51.77.58.92
DB_PORT=1993
DB_USER=pawwasfx
DB_PASSWORD=pawwasfx123
DB_NAME=bazadanych

# MT5 - LOCAL (Choose one method)
MT5_ACCOUNT_LOCAL=your_account_number
MT5_PASSWORD_LOCAL=your_mt5_password
MT5_SERVER_LOCAL=your_broker_server

# OR MT5 - REMOTE (For VPS deployment)
MT5_REMOTE_ENABLED=true
MT5_REMOTE_HOST=your_vps_ip
MT5_REMOTE_USER=your_vps_user
MT5_REMOTE_PASSWORD=your_vps_password
# OR use SSH key instead:
MT5_REMOTE_SSH_KEY=/path/to/private/key

# TRADING
INITIAL_CAPITAL=100000
MAX_STRATEGIES=50

# RISK PARAMETERS
MAX_DAILY_LOSS_PCT=5
DRAWDOWN_CRITICAL=12

# RL CONFIGURATION
RL_ENABLED=true
RL_MODEL_TYPE=PPO
RL_LEARNING_RATE=0.0003
```

### Step 5: Initialize Database
```bash
python -c "from database import initialize_database; initialize_database()"
```

Expected output:
```
✅ Database schema initialized
✅ Connected to PostgreSQL (51.77.58.92:1993/bazadanych)
```

### Step 6: Verify MT5 Connection
```bash
python mt5_connector.py
```

Expected output (local):
```
💻 Using LOCAL MT5
✅ Connected to LOCAL MT5
  Balance: $100,000.00
  Equity: $100,000.00
  Free Margin: $99,500.00
```

OR (remote):
```
🌐 Using REMOTE MT5 (VPS/Server)
✅ SSH connected via password
✅ Connected to REMOTE MT5 (your_vps_ip)
```

## 🎯 Quick Start

### 1. Load Existing Strategies
```python
from strategy_framework import StrategyRegistry

registry = StrategyRegistry()
print(f"Loaded {len(registry.strategies)} strategies")
```

### 2. Run Live Trading
```python
python main.py --mode live --symbols XAUUSD NASDAQ
```

### 3. Backtest Strategy
```python
from backtester import Backtester
from datetime import datetime

backtester = Backtester(
    start_date=datetime(2023, 1, 1),
    end_date=datetime(2024, 1, 1)
)

# Get backtest results
result = backtester.backtest_strategy(strategy, "XAUUSD")
metrics = result.calculate_metrics()
print(f"Win Rate: {metrics['win_rate']:.1%}")
print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
```

### 4. Train RL Agent
```python
from rl_engine import RLTrainer

trainer = RLTrainer(symbols=["XAUUSD"], model_type="PPO")
trainer.train_all(total_timesteps=50000)
```

### 5. Launch Dashboard
```bash
python dashboard.py
# Navigate to http://localhost:8050
```

## 🔌 Remote MT5 Setup (VPS)

### On Your VPS:

1. **Install MetaTrader5 on VPS**
   ```bash
   # Follow official MT5 Linux installation
   # Or use Windows VPS with native MT5 terminal
   ```

2. **Copy Helper Scripts to VPS**
   ```bash
   scp -r remote_mt5_scripts/* user@vps_ip:/home/user/mt5_helpers/
   ```

3. **Install Python on VPS**
   ```bash
   apt-get update && apt-get install python3 python3-pip
   pip3 install MetaTrader5 pandas
   ```

4. **Test Remote Scripts**
   ```bash
   ssh user@vps_ip
   cd ~/mt5_helpers
   python3 get_balance.py  # Should return account info
   ```

### Configure SSH Connection:

**Option 1: Password Authentication**
```env
MT5_REMOTE_ENABLED=true
MT5_REMOTE_HOST=your_vps_ip
MT5_REMOTE_PORT=22
MT5_REMOTE_USER=your_vps_user
MT5_REMOTE_PASSWORD=your_vps_password
MT5_REMOTE_PATH=/home/user/mt5_helpers
```

**Option 2: SSH Key Authentication** (More Secure)
```bash
# Generate SSH key locally (if you don't have one)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa

# Copy public key to VPS
ssh-copy-id -i ~/.ssh/id_rsa.pub user@vps_ip

# Configure in .env
MT5_REMOTE_ENABLED=true
MT5_REMOTE_HOST=your_vps_ip
MT5_REMOTE_PORT=22
MT5_REMOTE_USER=your_vps_user
MT5_REMOTE_SSH_KEY=/home/youruser/.ssh/id_rsa
MT5_REMOTE_PATH=/home/user/mt5_helpers
```

## 📁 Project Structure

```
portfolio-manager-pro/
├── config.py                      # Configuration management
├── database.py                    # PostgreSQL ORM
├── mt5_connector.py              # MT5 integration (local + remote)
├── strategy_framework.py         # Strategy engine
├── risk_manager.py              # Risk management
├── rl_engine.py                 # RL agent & environment
├── backtester.py                # Backtesting engine
├── dashboard.py                 # Real-time monitoring UI
├── logging_system.py            # Audit & compliance logging
├── main.py                      # Orchestrator
│
├── remote_mt5_scripts/          # VPS helper scripts
│   ├── get_candles.py
│   ├── get_price.py
│   ├── place_order.py
│   ├── get_balance.py
│   └── get_positions.py
│
├── requirements.txt             # Python dependencies
├── .env.example                # Configuration template
├── ARCHITECTURE.md             # System design document
├── INSTALLATION.md             # This file
├── PROGRESS.md                # Development progress
└── logs/                       # Runtime logs & audit trail
```

## 🧪 Testing

### Unit Tests
```bash
pytest tests/ -v
```

### Database Connection Test
```bash
python -c "from database import Database; db = Database(); print('✅ Connected')"
```

### MT5 Connectivity Test
```bash
python mt5_connector.py
```

### Strategy Execution Test
```bash
python -c "from strategy_framework import StrategyRegistry; r = StrategyRegistry(); print(f'✅ {len(r.strategies)} strategies loaded')"
```

## 🔒 Security Considerations

1. **Never commit `.env` file** - Always use `.env.example` template
2. **Use SSH keys for remote MT5** - Avoid storing passwords in `.env`
3. **Restrict database access** - Use firewall rules to limit PostgreSQL access
4. **Audit logging** - All trades & risk checks are logged in database
5. **Regular backups** - Backup PostgreSQL database weekly

## 📊 Monitoring & Maintenance

### Check System Status
```bash
# View logs
tail -f logs/portfolio_manager.log

# Check recent trades
python -c "from database import Database; db = Database(); print(db.get_open_trades())"

# Monitor RL training
python -c "from database import Database; db = Database(); print(db.get_rl_history(limit=10))"
```

### Update Strategies
```python
from database import Database
from strategy_framework import StrategyRegistry, RSIStrategy

db = Database()
registry = StrategyRegistry()

# Add new strategy
new_strategy = RSIStrategy(
    name="RSI_Updated",
    symbol="NASDAQ",
    timeframe=60,
    config={'period': 16, 'overbought': 72, 'oversold': 28}
)

strategy_id = registry.add_strategy(new_strategy)
```

## 🚀 Deployment Checklist

- [ ] Database configured and initialized
- [ ] MT5 connection tested (local or remote)
- [ ] All dependencies installed
- [ ] `.env` file configured with credentials
- [ ] Remote MT5 scripts deployed to VPS (if using remote)
- [ ] SSH key authentication set up (if using remote)
- [ ] Initial backtest passed
- [ ] Dashboard accessible
- [ ] Logging system active
- [ ] Risk parameters reviewed
- [ ] First live paper trade executed
- [ ] Monitoring alerts configured

## 📞 Troubleshooting

### MT5 Connection Failed
```
Error: MT5 initialization failed
Solution:
1. Verify MetaTrader5 is installed and running
2. Check account credentials in .env
3. Ensure firewall allows MT5 API connections
```

### Database Connection Error
```
Error: Database connection failed
Solution:
1. Verify PostgreSQL is running on 51.77.58.92:1993
2. Check credentials: pawwasfx / pawwasfx123
3. Test with: psql -h 51.77.58.92 -U pawwasfx -d bazadanych
```

### Remote MT5 SSH Error
```
Error: SSH connection failed
Solution:
1. Verify VPS IP and credentials
2. Test SSH: ssh user@vps_ip
3. Verify MT5 helper scripts are on VPS
4. Check SSH key permissions: chmod 600 ~/.ssh/id_rsa
```

### RL Training Slow
```
Optimization:
1. Reduce total_timesteps in trainer.train_all()
2. Use smaller lookback window
3. Run on GPU if available (enable CUDA in config)
```

## 📖 Additional Resources

- **Architecture**: See `ARCHITECTURE.md` for detailed system design
- **Progress**: See `PROGRESS.md` for development status
- **Configuration**: See `config.py` for all available parameters
- **Database Schema**: See `database.py` for table definitions

## 🎓 Next Steps

1. **Paper Trading**: Run 1 week of paper trading to validate
2. **Backtesting**: Test strategies on 1+ years of historical data
3. **RL Training**: Train agent for 50k+ steps
4. **Risk Validation**: Verify risk limits are enforced
5. **Live Deployment**: Start with small capital, scale gradually

---

**Support**: For issues or questions, check the logs in `./logs/` directory or review error messages in the console output.

**Version**: Portfolio Manager Pro v1.0
**Last Updated**: 2024-11-07
