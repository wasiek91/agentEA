================================================================================
  TRADING ANALYTICS + POSTGRESQL MONITORING - DEPLOYMENT PACK
  Wersja 2.0.0 | 2025-11-04
================================================================================

Ten folder zawiera wszystkie pliki potrzebne do uruchomienia aplikacji
na serwerze Ubuntu wraz z monitoringiem PostgreSQL.

================================================================================
  ZAWARTOŚĆ FOLDERU
================================================================================

DOKUMENTACJA:
  - README_START_HERE.txt       - Ten plik (zacznij tutaj!)
  - DEPLOY_GUIDE.md             - Szczegółowy przewodnik wdrożenia
  - MONITORING_POSTGRES.md      - Dokumentacja monitoringu bazy danych
  - INSTRUKCJA_DEPLOY.txt       - Skrócona instrukcja (PL)

BACKEND:
  - backend_fastapi_mt5.py      - Główna aplikacja FastAPI
  - start_backend.sh            - Skrypt uruchamiający backend

MONITORING:
  - monitor_postgres.py         - Skrypt monitoringu PostgreSQL (Python)
  - monitor_postgres.sh         - Skrypt monitoringu (Bash dla Ubuntu)

INSTALACJA:
  - setup_monitoring.sh         - Automatyczna instalacja monitoringu
  - install_ubuntu.sh           - Instalacja głównej aplikacji
  - install_service.sh          - Instalacja systemd service

BAZA DANYCH:
  - database_schema.sql         - Schemat bazy danych
  - migrations_mt5_positions.sql - Migracje MT5
  - run_migration_ubuntu.py     - Skrypt migracji

KONFIGURACJA:
  - requirements_ubuntu.txt     - Zależności Python (główne)
  - requirements_mt5_simple.txt - Zależności MT5
  - requirements_mt5_sync.txt   - Zależności synchronizacji

================================================================================
  SZYBKI START
================================================================================

1. PRZYGOTOWANIE (na Windows)
   -----------------------------
   a) Upewnij się, że masz dane dostępowe do serwera Ubuntu:
      - Adres IP lub domena
      - Użytkownik SSH
      - Hasło lub klucz SSH

   b) Upewnij się, że masz credentials do bazy danych:
      - DATABASE_URL
      - SUPABASE_URL (jeśli używasz Supabase)
      - SUPABASE_ANON_KEY

2. TRANSFER PLIKÓW
   ----------------
   Wybierz jedną z metod:

   A) SCP (z Windows PowerShell lub Git Bash):
      scp -r * user@server-ip:/home/user/trading-analytics/

   B) WinSCP (GUI):
      - Otwórz WinSCP
      - Połącz się SFTP
      - Przeciągnij wszystkie pliki

   C) FileZilla:
      - Protokół: SFTP
      - Połącz i prześlij pliki

3. INSTALACJA NA UBUNTU
   ---------------------
   a) Połącz się SSH:
      ssh user@server-ip

   b) Przejdź do katalogu:
      cd ~/trading-analytics

   c) Uruchom instalację:
      chmod +x setup_monitoring.sh
      ./setup_monitoring.sh

   d) Konfiguruj .env:
      nano .env
      (wklej swoje credentials i zapisz: Ctrl+O, Enter, Ctrl+X)

4. URUCHOMIENIE
   -------------
   a) Test połączenia z bazą:
      source venv/bin/activate
      python3 monitor_postgres.py health

   b) Uruchom backend:
      sudo systemctl start trading-analytics
      sudo systemctl status trading-analytics

   c) Uruchom monitoring:
      sudo systemctl start postgres-monitor
      sudo systemctl status postgres-monitor

5. WERYFIKACJA
   ------------
   a) Sprawdź API:
      curl http://localhost:8000/health

   b) Sprawdź monitoring:
      ./monitor_postgres.sh

   c) Zobacz logi:
      tail -f logs/backend.log

================================================================================
  STRUKTURA PO INSTALACJI
================================================================================

/home/user/trading-analytics/
├── venv/                        # Wirtualne środowisko Python
├── logs/                        # Logi aplikacji i monitoringu
├── backend_fastapi_mt5.py       # Backend
├── monitor_postgres.py          # Monitoring
├── .env                         # Konfiguracja (UTWÓRZ TO!)
└── ...

================================================================================
  WAŻNE PLIKI DO UTWORZENIA
================================================================================

1. .env (WYMAGANE!)
   -----------------
   Utwórz plik .env na serwerze Ubuntu:

   DATABASE_URL=postgresql://user:password@host:5432/database
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-anon-key
   FASTAPI_SECRET_KEY=your-secret-key-min-32-chars
   ENVIRONMENT=production

================================================================================
  KOMENDY PO INSTALACJI
================================================================================

BACKEND:
  sudo systemctl start trading-analytics    - Uruchom backend
  sudo systemctl stop trading-analytics     - Zatrzymaj backend
  sudo systemctl status trading-analytics   - Status backend
  sudo systemctl restart trading-analytics  - Restart backend

MONITORING:
  ./monitor_postgres.sh                     - Raport monitoringu
  ./monitor_postgres.sh health              - Health check
  ./monitor_postgres.sh continuous 60       - Monitoring ciągły (60s)
  python3 monitor_postgres.py health        - Python health check

LOGI:
  tail -f logs/backend.log                  - Logi backend
  tail -f logs/monitor_service.log          - Logi monitoringu
  sudo journalctl -u trading-analytics -f   - System logs backend

BAZA DANYCH:
  psql "$DATABASE_URL" -c "SELECT version()"  - Test połączenia
  python3 monitor_postgres.py queries         - Aktywne zapytania

================================================================================
  AUTOMATYZACJA
================================================================================

Po instalacji automatycznie skonfigurowane:

1. SYSTEMD SERVICES
   - trading-analytics.service  (backend)
   - postgres-monitor.service   (monitoring)
   Autostart: sudo systemctl enable [service-name]

2. CRON JOBS (opcjonalne, konfigurowane podczas setup)
   - Health check co 5 minut
   - Raport co godzinę
   - Daily backup (opcjonalny)

3. LOGI
   - Rotacja logów
   - Automatyczne czyszczenie starych logów

================================================================================
  PORTY I DOSTĘP
================================================================================

Backend API:    http://localhost:8000
API Docs:       http://localhost:8000/docs
Health Check:   http://localhost:8000/health

Jeśli używasz Nginx:
  http://your-domain.com
  https://your-domain.com (z SSL)

================================================================================
  BEZPIECZEŃSTWO
================================================================================

1. FIREWALL
   sudo ufw allow 22    # SSH
   sudo ufw allow 80    # HTTP
   sudo ufw allow 443   # HTTPS
   sudo ufw enable

2. SSL (z Let's Encrypt)
   sudo certbot --nginx -d your-domain.com

3. BACKUP
   Automatyczny backup bazy danych:
   - Konfigurowany w cron
   - Przechowywany w ~/backups
   - Retencja 7 dni

================================================================================
  MONITORING
================================================================================

Dostępne metryki:
  - Database health & size
  - Connections (total, active, idle)
  - Long running queries
  - Cache hit ratio
  - Table & index statistics
  - System resources (CPU, RAM, Disk)

Alerty:
  - Email alerts (konfiguracja w .env)
  - Slack webhooks (opcjonalnie)
  - Telegram bots (opcjonalnie)

================================================================================
  ROZWIĄZYWANIE PROBLEMÓW
================================================================================

Problem: Backend nie startuje
  Rozwiązanie:
    - Sprawdź logi: sudo journalctl -u trading-analytics -n 50
    - Sprawdź .env: cat .env
    - Test bazy: psql "$DATABASE_URL" -c "SELECT 1"

Problem: Nie można połączyć się z bazą
  Rozwiązanie:
    - Sprawdź DATABASE_URL w .env
    - Test: python3 monitor_postgres.py health
    - Sprawdź firewall na serwerze bazy danych

Problem: Monitoring nie działa
  Rozwiązanie:
    - Sprawdź uprawnienia: ls -la monitor_postgres.sh
    - Test: ./monitor_postgres.sh health
    - Sprawdź logi: tail -f logs/monitor_service_error.log

================================================================================
  DOKUMENTACJA SZCZEGÓŁOWA
================================================================================

Przeczytaj szczegółowe przewodniki:

1. DEPLOY_GUIDE.md
   - Pełny przewodnik wdrożenia krok po kroku
   - Wszystkie metody instalacji
   - Konfiguracja Nginx + SSL
   - Backup i recovery

2. MONITORING_POSTGRES.md
   - Kompletna dokumentacja monitoringu
   - Wszystkie metryki i progi alertów
   - Integracje (Prometheus, Grafana, pgAdmin)
   - Najlepsze praktyki

3. INSTRUKCJA_DEPLOY.txt
   - Skrócona instrukcja po polsku
   - Quick reference

================================================================================
  WSPARCIE
================================================================================

W razie problemów:
  1. Sprawdź logi w katalogu logs/
  2. Uruchom diagnostykę: ./monitor_postgres.sh health
  3. Przeczytaj DEPLOY_GUIDE.md
  4. Sprawdź status services: sudo systemctl status trading-analytics

================================================================================
  CHECKLIST WDROŻENIA
================================================================================

[ ] Przesłano wszystkie pliki na serwer
[ ] Uruchomiono setup_monitoring.sh
[ ] Utworzono i skonfigurowano .env
[ ] Przetestowano połączenie z bazą danych
[ ] Backend działa (systemctl status trading-analytics)
[ ] Monitoring działa (systemctl status postgres-monitor)
[ ] API odpowiada: curl http://localhost:8000/health
[ ] Skonfigurowano cron jobs
[ ] Skonfigurowano firewall
[ ] Przetestowano restart serwera
[ ] Skonfigurowano backupy (opcjonalnie)
[ ] Skonfigurowano Nginx + SSL (opcjonalnie)

================================================================================

Powodzenia z wdrożeniem!

Jeśli wszystko działa poprawnie, powinieneś zobaczyć:
  - Backend dostępny na porcie 8000
  - Monitoring zapisujący raporty co godzinę
  - Automatyczne backupy uruchamiające się codziennie
  - System działający stabilnie 24/7

================================================================================
