# ⏭️ Next Session - Quick Start

## 🔧 TO-DO NA NASTĘPNĄ SESJĘ

```bash
# 1. Przejdź do folderu
cd C:\Users\HP\OneDrive\Pulpit\Cloude\janosik-ea

# 2. Zainstaluj requirements
pip install -r requirements.txt

# 3. Skopuj .env
copy .env.example .env

# 4. Edytuj .env - dodaj MT5 credentials
# MT5_ACCOUNT=your_account_number
# MT5_PASSWORD=your_password
# MT5_SERVER=your_server_name
```

---

## 📋 PostgreSQL Connection Test

```python
# 1. Test connection (uruchom w Python)
from core_database import setup_database, Database

# Setup tables
setup_database()

# Test connection
db = Database()
active_strategies = db.get_active_strategies()
print(active_strategies)
db.close()
```

**Expected Output:**
```
✅ Connected to PostgreSQL: bazadanych
✅ Database schema created/verified
```

---

## 🔍 Informacje Potrzebne

### 1. **Strategie z Twojego Portfolio**
Przygotuj plik lub listę:
```
Strategia #1:
- Nazwa: RSI_Overbought
- Typ: RSI Crossover
- Parametry: RSI_period=14, Overbought=70, Oversold=30
- Entry: Gdy RSI < 30
- Exit: Gdy RSI > 70
- TP: +100 pips
- SL: -50 pips
- Performance: XX% win rate

Strategia #2:
... (itd.)
```

### 2. **RL Configuration**

Odpowiedz na pytania:

**State Space** (co obserwować?):
```
- [ ] Current price
- [ ] RSI indicator
- [ ] MACD indicator
- [ ] Volume
- [ ] Portfolio equity
- [ ] Open positions count
- [ ] Drawdown %
- [ ] Other?
```

**Action Space** (jakie akcje?):
```
- [ ] BUY_SMALL (0.5 lot)
- [ ] BUY_MEDIUM (1.0 lot)
- [ ] BUY_LARGE (1.5 lot)
- [ ] SELL_SMALL
- [ ] SELL_MEDIUM
- [ ] SELL_LARGE
- [ ] HOLD
- [ ] CLOSE_ALL
```

**Reward Function** (co to "dobra" decyzja?):
```
Base Reward = Profit/Loss
Bonus/Penalty:
- +10 if win
- -5 if loss
- -2 * (current_drawdown / max_drawdown) [penalty]
- +1 if risk_reward_ratio > 1.5
```

### 3. **MT5 Account (dla config.py)**
```
MT5_ACCOUNT = XXXXX (Twój account number)
MT5_PASSWORD = (Twoje hasło do MT5)
MT5_SERVER = (Nazwa serwera brokera, np "FTMO-Demo")
```

---

## 📝 Pliki do Modyfikacji

### `.env` (after copying from .env.example)
```ini
# PostgreSQL - JUŻ USTAWIONO ✅
DB_HOST=51.77.58.92
DB_PORT=1993
DB_USER=pawwasfx
DB_PASSWORD=pawwasfx123
DB_NAME=bazadanych

# MT5 - WYMAGA UZUPEŁNIENIA
MT5_ACCOUNT=YOUR_ACCOUNT_NUMBER  # ← Dodaj
MT5_PASSWORD=YOUR_PASSWORD        # ← Dodaj
MT5_SERVER=YOUR_SERVER_NAME       # ← Dodaj
```

---

## 🎯 Implementation Order

1. ✅ **Setup** (2 min)
   - pip install
   - Copy .env
   - Fill MT5 credentials

2. ✅ **Test** (5 min)
   - Test PostgreSQL connection
   - Test MT5 connection
   - Get account balance

3. ✅ **Strategies** (30 min)
   - Create strategy_loader.py
   - Load strategies from DB
   - Execute on latest candles

4. ✅ **RL** (60 min)
   - Build Gym environment
   - Implement reward function
   - Create DQN/PPO agent

5. ✅ **Risk Manager** (30 min)
   - Drawdown monitoring
   - Position sizing
   - Hedge logic

6. ✅ **Integration** (30 min)
   - Connect all modules
   - Run backtester
   - Test on live data

---

## 🚀 Session 1 Recap

**✅ Completed:**
- Full project structure designed
- 3 core modules built (config, database, mt5)
- PostgreSQL credentials configured
- Database schema designed
- Project plan documented

**⏳ Waiting For:**
- PostgreSQL connection test
- Strategy definitions
- RL specifications
- MT5 account details

**Commit Hash**: `6ac6532` (Janosik EA initialization)

---

## 📞 Questions Before Starting?

If anything unclear:
1. Check `PROJECT_STRUCTURE.md` for architecture
2. Check `PROGRESS_SUMMARY.md` for full status
3. Run `config.py` to validate setup

Ready to code! 🔥🤖
