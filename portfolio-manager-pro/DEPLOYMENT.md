# 🚀 Distributed Deployment Guide - Portfolio Manager Pro

## Architektura Distributed

```
┌─ TWOJA MASZYNA (LOCAL) ────────────────────┐
│ Claude Code / CLI Manager                   │
│ - Interactive terminal                      │
│ - Zarządza & decyduje                       │
│ - Wysyła komendy na serwer                  │
│ - Monitoruje status LIVE                    │
└──────────────────┬──────────────────────────┘
                   │ SSH / REST API / WebSocket
                   ↓
┌─ SERWER (VPS / CLOUD) ─────────────────────┐
│ Portfolio Manager Pro (Daemon)              │
│ - api_server.py (FastAPI port 8000)        │
│ - main.py live trading loop                │
│ - MT5 terminal running                     │
│ - Collecting metrics continuously          │
└──────────────────┬──────────────────────────┘
                   │
                   ↓
        ┌──────────────────────┐
        │  PostgreSQL 51.77.   │
        │  58.92:1993          │
        │  bazadanych          │
        └──────────────────────┘
```

---

## 📋 KROK 1: Przygotowanie Serwera (VPS)

### 1.1 Zaloguj się na serwer
```bash
ssh user@your_vps_ip
# lub Windows: ssh -i "private_key.pem" user@your_vps_ip
```

### 1.2 Zainstaluj zależności
```bash
# Python
sudo apt-get update
sudo apt-get install python3.9 python3-pip python3-venv

# MT5 (jeśli Linux)
# Lub użyj Windows VPS z MT5 terminal zainstalowanym

# Git
sudo apt-get install git
```

### 1.3 Sklonuj Portfolio Manager Pro
```bash
cd /home/user  # lub twój katalog
git clone https://github.com/yourusername/portfolio-manager-pro.git
cd portfolio-manager-pro
```

### 1.4 Utwórz virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 1.5 Skonfiguruj .env na serwerze
```bash
cp .env.example .env
nano .env  # edytuj poniższe wartości
```

**.env na serwerze:**
```env
# DATABASE
DB_HOST=51.77.58.92
DB_PORT=1993
DB_USER=pawwasfx
DB_PASSWORD=pawwasfx123
DB_NAME=bazadanych

# MT5 - REMOTE (jeśli serwer ma MT5)
MT5_REMOTE_ENABLED=false  # bo on jest na serwerze, używa lokalnie
MT5_ACCOUNT_LOCAL=your_account_number
MT5_PASSWORD_LOCAL=your_password
MT5_SERVER_LOCAL=your_broker_server

# API SERVER
API_HOST=0.0.0.0  # Nasłuchuj na wszystkich interfejsach
API_PORT=8000
API_KEY=your_secret_key_here  # Dla bezpieczeństwa

# TRADING
INITIAL_CAPITAL=100000
```

### 1.6 Inicjalizuj bazę danych
```bash
python -c "from database import initialize_database; initialize_database()"
```

---

## 📋 KROK 2: Uruchomienie API Server na Serwerze

### 2.1 Uruchom API server
```bash
# W tle (screen/tmux)
screen -S pmp-api
python api_server.py
# Ctrl+A D aby odłączyć
```

### 2.2 Lub użyj systemd service (lepiej)
Stwórz `/etc/systemd/system/pmp-api.service`:

```ini
[Unit]
Description=Portfolio Manager Pro API
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/home/your_user/portfolio-manager-pro
Environment="PATH=/home/your_user/portfolio-manager-pro/venv/bin"
ExecStart=/home/your_user/portfolio-manager-pro/venv/bin/python api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Uruchom:
```bash
sudo systemctl daemon-reload
sudo systemctl enable pmp-api
sudo systemctl start pmp-api
sudo systemctl status pmp-api
```

### 2.3 Uruchom live trading
Stwórz `/home/user/pmp-trading.sh`:
```bash
#!/bin/bash
cd /home/user/portfolio-manager-pro
source venv/bin/activate
python main.py --mode live --symbols XAUUSD NASDAQ
```

Lub jako systemd service (`pmp-trading.service`):
```ini
[Unit]
Description=Portfolio Manager Pro Trading Bot
After=pmp-api.service

[Service]
Type=simple
User=your_user
WorkingDirectory=/home/your_user/portfolio-manager-pro
Environment="PATH=/home/your_user/portfolio-manager-pro/venv/bin"
ExecStart=/home/your_user/portfolio-manager-pro/venv/bin/python main.py --mode live --symbols XAUUSD NASDAQ
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 🔌 KROK 3: Konfiguracja SSH Tunnel (Bezpieczeństwo)

### 3.1 Utwórz SSH tunnel z lokalnej maszyny do serwera

```bash
# Windows (PowerShell)
ssh -L 8000:localhost:8000 user@your_vps_ip

# Linux/Mac
ssh -L 8000:localhost:8000 -N user@your_vps_ip
```

To zmapuje port 8000 serwera do localhost:8000 na Twojej maszynie.

### 3.2 Alternatywnie: Otwórz port w firewall
```bash
# Na serwerze
sudo ufw allow 8000/tcp
```

---

## 💻 KROK 4: CLI Manager na Twojej Maszynie

### 4.1 Zainstaluj CLI Manager lokalnie
```bash
# Skopiuj cli_manager.py do swojego projektu
cp portfolio-manager-pro/cli_manager.py ~/my-trading-cli/

pip install typer rich requests
```

### 4.2 Użyj CLI Managera (przykłady)

```bash
# 1. Sprawdź status
python cli_manager.py status

# 2. Sprawdź health
python cli_manager.py health

# 3. Uruchom trading
python cli_manager.py start --symbols XAUUSD,NASDAQ

# 4. Wyświetl pozycje
python cli_manager.py positions

# 5. Wyświetl strategie
python cli_manager.py strategies

# 6. Włącz strategię
python cli_manager.py enable 1

# 7. Wyświetl transakcje
python cli_manager.py trades --limit 30 --days 7

# 8. Metryki ryzyka
python cli_manager.py risk

# 9. Cena symbolu
python cli_manager.py price XAUUSD

# 10. Złóż ręczne zlecenie
python cli_manager.py order XAUUSD BUY 1.5 --tp 2050 --sl 1950

# 11. 🚨 EMERGENCY STOP
python cli_manager.py emergency

# 12. Wszystkie komendy
python cli_manager.py commands
```

### 4.3 Custom API URL (jeśli nie localhost)
```bash
# Jeśli serwer ma publiczny IP
python cli_manager.py status --api http://your_vps_ip:8000

# Lub z SSH tunnel (preferred)
python cli_manager.py status --api http://localhost:8000
```

---

## 🔒 Bezpieczeństwo

### SSL/HTTPS Certificate (production)
```bash
# Na serwerze
sudo apt-get install certbot python3-certbot-nginx

# Zdobądź certyfikat
sudo certbot certonly --standalone -d your_domain.com

# Zaktualizuj api_server.py aby używał HTTPS
# Lub użyj Nginx jako reverse proxy
```

### Firewall Rules
```bash
# Zezwól tylko SSH i API
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 8000/tcp  # API
```

### API Key (w przyszłości)
Dodaj Bearer token authentication do api_server.py:
```python
@app.middleware("http")
async def verify_api_key(request, call_next):
    if request.url.path in ["/health"]:
        return await call_next(request)

    api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
    if api_key != settings.API_KEY:
        return JSONResponse(status_code=401, content={"detail": "Invalid API key"})

    return await call_next(request)
```

---

## 📊 Monitorowanie

### Logi systemd
```bash
# Sprawdź logi API
sudo journalctl -u pmp-api -f

# Sprawdź logi tradingu
sudo journalctl -u pmp-trading -f

# Ostatnie 100 linii
sudo journalctl -u pmp-api -n 100
```

### Monitory (na serwerze)
```bash
# Sprawdź procesy
ps aux | grep python

# Użycie CPU/Memory
top

# Połączenie do bazy danych
netstat -tnp | grep 51.77.58.92
```

---

## 🔄 Workflow - Zarządzanie z CLI

### Typowy dzień pracy

```bash
# 1. Rano - Start
python cli_manager.py status                    # Sprawdź status
python cli_manager.py start                     # Uruchom trading

# 2. W ciągu dnia - Monitor
python cli_manager.py positions                 # Otwarte pozycje
python cli_manager.py trades --limit 10         # Ostatnie transakcje
python cli_manager.py risk                      # Metryki ryzyka

# 3. Jeśli potrzebne ręczne działania
python cli_manager.py price XAUUSD              # Sprawdź cenę
python cli_manager.py order XAUUSD BUY 1.0      # Złóż ręczne zlecenie
python cli_manager.py close-pos 5               # Zamknij pozycję

# 4. Po rynku - Stop
python cli_manager.py stop                      # Zatrzymaj trading
python cli_manager.py status                    # Finalne podsumowanie
```

---

## 🛠️ Troubleshooting

### Problem: "Connection refused"
```
Rozwiązanie:
1. Sprawdzić czy API server działa: curl http://localhost:8000/health
2. Sprawdzić firewall: sudo ufw status
3. Sprawdzić port: sudo ss -tnlp | grep 8000
```

### Problem: "Database connection failed"
```
Rozwiązanie:
1. Sprawdzić .env: DB_HOST, DB_PORT, DB_USER, DB_PASSWORD
2. Test z serwera: psql -h 51.77.58.92 -U pawwasfx -d bazadanych
3. Sprawdzić firewall dostęp do bazy
```

### Problem: "MT5 initialization failed"
```
Rozwiązanie:
1. Sprawdzić czy MT5 terminal jest otwarty
2. Sprawdzić credentials w .env (MT5_ACCOUNT_LOCAL, MT5_PASSWORD_LOCAL)
3. Sprawdzić connection do brokera
```

### Problem: API jest wolny
```
Rozwiązanie:
1. Dodać caching do popularnychendpoints
2. Użyć Redis cache
3. Optimizować database queries
```

---

## 📈 Performance Tips

1. **Baza danych**: Indeksy na `entry_time`, `symbol`, `status`
2. **API**: Użyć async/await dla long-running tasks
3. **Serwer**: Monitor CPU/RAM, scale horizontally jeśli potrzeba
4. **Logs**: Archiwizuj stare logi, nie trzymaj na dysku za długo

---

## 🚀 Deployment Checklist

- [ ] VPS/Cloud konto aktywne
- [ ] Python 3.9+ zainstalowany
- [ ] Portfolio Manager Pro sklonowany
- [ ] Virtualenv i requirements zainstalowane
- [ ] .env skonfigurowany
- [ ] Baza danych zainicjalizowana
- [ ] MT5 terminal uruchomiony na serwerze
- [ ] API server działa (curl test)
- [ ] SSH tunnel skonfigurowany
- [ ] CLI Manager zainstalowany lokalnie
- [ ] Test: `cli_manager.py status` zwraca dane
- [ ] Systemd services skonfigurowane (auto-restart)
- [ ] Firewall rules ustawione
- [ ] Backups bazy danych ustawione
- [ ] Monitoring setup (opcjonalnie)

---

## 📞 Support & Next Steps

1. Test API: `curl http://localhost:8000/docs` → Swagger UI
2. Monitor logi: `sudo journalctl -u pmp-api -f`
3. Uruchom paper trading: `cli_manager.py start`
4. Obserwuj pozycje: `cli_manager.py positions`

**Status**: Gotowy do live deployment 🎉
