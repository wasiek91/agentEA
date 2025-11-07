"""CLI Manager - Zarządzaj Portfolio Manager Pro z lokalnego terminala."""
import requests
import json
import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from datetime import datetime
import time

console = Console()
app = typer.Typer()


class PMPClient:
    """Klient API do komunikacji z Portfolio Manager Pro."""

    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.timeout = 10

    def _request(self, method: str, endpoint: str, **kwargs):
        """Wykonaj HTTP request."""
        try:
            url = f"{self.api_url}{endpoint}"
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            console.print(f"[red]❌ Błąd połączenia: Nie mogę połączyć się z API ({self.api_url})[/red]")
            raise
        except requests.exceptions.HTTPError as e:
            console.print(f"[red]❌ Błąd API: {e.response.text}[/red]")
            raise
        except Exception as e:
            console.print(f"[red]❌ Błąd: {str(e)}[/red]")
            raise

    def health_check(self):
        return self._request("GET", "/health")

    def get_status(self):
        return self._request("GET", "/status")

    def start_trading(self, symbols: List[str] = None):
        return self._request("POST", "/trading/start", json={"symbols": symbols})

    def stop_trading(self):
        return self._request("POST", "/trading/stop")

    def emergency_stop(self):
        return self._request("POST", "/trading/emergency-stop")

    def get_strategies(self):
        return self._request("GET", "/strategies")

    def enable_strategy(self, strategy_id: int):
        return self._request("POST", f"/strategies/{strategy_id}/enable")

    def disable_strategy(self, strategy_id: int):
        return self._request("POST", f"/strategies/{strategy_id}/disable")

    def get_positions(self):
        return self._request("GET", "/positions")

    def close_position(self, position_id: int, exit_price: Optional[float] = None):
        return self._request("POST", f"/positions/{position_id}/close", json={"exit_price": exit_price})

    def get_trades(self, limit: int = 50, days: int = 30):
        return self._request("GET", "/trades", params={"limit": limit, "days": days})

    def get_risk_metrics(self):
        return self._request("GET", "/risk/metrics")

    def validate_trade(self, symbol: str, direction: str, lot_size: float, entry_price: float):
        return self._request("POST", "/risk/validate-trade", json={
            "symbol": symbol,
            "direction": direction,
            "lot_size": lot_size,
            "entry_price": entry_price
        })

    def get_candles(self, symbol: str, timeframe: int = 60, count: int = 100):
        return self._request("GET", f"/market/candles/{symbol}", params={
            "timeframe": timeframe,
            "count": count
        })

    def get_price(self, symbol: str):
        return self._request("GET", f"/market/price/{symbol}")

    def place_order(self, symbol: str, direction: str, lot_size: float, price: float = 0,
                   take_profit: float = 0, stop_loss: float = 0):
        return self._request("POST", "/manual/place-order", json={
            "symbol": symbol,
            "direction": direction,
            "lot_size": lot_size,
            "price": price,
            "take_profit": take_profit,
            "stop_loss": stop_loss
        })

    def run_backtest(self, strategy_name: str, symbol: str, start_date: str, end_date: str):
        return self._request("POST", "/backtest", json={
            "strategy_name": strategy_name,
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date
        })

    def start_rl_training(self, symbols: List[str] = None, timesteps: int = 50000, model_type: str = "PPO"):
        return self._request("POST", "/rl/train", json={
            "symbols": symbols,
            "timesteps": timesteps,
            "model_type": model_type
        })

    def get_audit_trail(self, event_type: Optional[str] = None, days: int = 7):
        return self._request("GET", "/audit/trail", params={
            "event_type": event_type,
            "days": days
        })


# Global client
client = PMPClient()


# ========== GŁÓWNE KOMENDY ==========

@app.command()
def status(api_url: str = typer.Option("http://localhost:8000", "--api")):
    """Sprawdź status systemu."""
    try:
        client.api_url = api_url
        status_data = client.get_status()

        panel = Panel(
            f"""
[bold cyan]📊 Portfolio Manager Pro - Status[/bold cyan]

[green]✅ System Online[/green]
Timestamp: {status_data['timestamp']}
Trading: {'[green]🟢 ACTIVE[/green]' if status_data['trading_active'] else '[red]🔴 STOPPED[/red]'}

[bold yellow]Metryki:[/bold yellow]
  Kapitał: ${status_data['equity']:,.2f}
  Drawdown: {status_data['drawdown']:.2f}% {status_data['drawdown_level']}
  Otwarte pozycje: {status_data['open_positions']}
  Aktywne strategie: {status_data['active_strategies']}
  Ostatnie transakcje: {status_data['recent_trades']}
  Win Rate: {status_data['win_rate']:.1f}%
            """,
            title="[bold]System Status[/bold]",
            border_style="cyan"
        )

        console.print(panel)

    except Exception as e:
        console.print(f"[red]❌ Błąd: {str(e)}[/red]")


@app.command()
def health(api_url: str = typer.Option("http://localhost:8000", "--api")):
    """Sprawdź health check."""
    try:
        client.api_url = api_url
        health_data = client.health_check()

        console.print(f"\n[green]✅ System Status: {health_data['status']}[/green]")
        console.print(f"Database: {health_data['database']}")
        console.print(f"MT5: {health_data['mt5']}")
        console.print(f"Trading Active: {health_data['trading_active']}\n")

    except Exception as e:
        console.print(f"[red]❌ System nie odpowiada[/red]")


# ========== TRADING CONTROL ==========

@app.command()
def start(
    symbols: Optional[str] = typer.Option(None, "--symbols", help="Symbole rozdzielone przecinkami"),
    api_url: str = typer.Option("http://localhost:8000", "--api")
):
    """Uruchom live trading."""
    try:
        client.api_url = api_url
        symbol_list = symbols.split(',') if symbols else None

        result = client.start_trading(symbol_list)
        console.print(f"\n[green]✅ Trading uruchomiony[/green]")
        console.print(f"Symbole: {result['symbols']}")
        console.print(f"Czas: {result['timestamp']}\n")

    except Exception as e:
        console.print(f"[red]❌ Błąd: {str(e)}[/red]")


@app.command()
def stop(api_url: str = typer.Option("http://localhost:8000", "--api")):
    """Zatrzymaj live trading."""
    if typer.confirm("Czy na pewno chcesz zatrzymać trading?"):
        try:
            client.api_url = api_url
            result = client.stop_trading()
            console.print(f"\n[yellow]🛑 Trading zatrzymany[/yellow]")
            console.print(f"Czas: {result['timestamp']}\n")

        except Exception as e:
            console.print(f"[red]❌ Błąd: {str(e)}[/red]")


@app.command()
def emergency(api_url: str = typer.Option("http://localhost:8000", "--api")):
    """🚨 EMERGENCY STOP - Zamknij wszystkie pozycje NATYCHMIAST."""
    if typer.confirm("🚨 EMERGENCY STOP! Zamknąć WSZYSTKIE pozycje?"):
        try:
            client.api_url = api_url
            result = client.emergency_stop()
            console.print(f"\n[bold red]🚨 EMERGENCY STOP WYKONANY[/bold red]")
            console.print(f"Zamknięte pozycje: {result['positions_closed']}\n")

        except Exception as e:
            console.print(f"[red]❌ Błąd: {str(e)}[/red]")


# ========== STRATEGIE ==========

@app.command()
def strategies(api_url: str = typer.Option("http://localhost:8000", "--api")):
    """Wyświetl strategie."""
    try:
        client.api_url = api_url
        data = client.get_strategies()

        table = Table(title="Aktywne Strategie")
        table.add_column("ID", style="cyan")
        table.add_column("Nazwa", style="magenta")
        table.add_column("Typ", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Alokacja", style="blue")
        table.add_column("Transakcje", style="white")
        table.add_column("Win Rate", style="white")

        for strategy in data['strategies']:
            status_emoji = "✅" if strategy['enabled'] else "❌"
            table.add_row(
                str(strategy['id']),
                strategy['name'],
                strategy['type'],
                status_emoji,
                f"{strategy['allocation']:.1f}%",
                str(strategy['total_trades']),
                f"{strategy['win_rate']:.1f}%"
            )

        console.print(table)
        console.print(f"\nTotal: {data['total']} strategii\n")

    except Exception as e:
        console.print(f"[red]❌ Błąd: {str(e)}[/red]")


@app.command()
def enable(
    strategy_id: int = typer.Argument(..., help="ID strategii"),
    api_url: str = typer.Option("http://localhost:8000", "--api")
):
    """Włącz strategię."""
    try:
        client.api_url = api_url
        result = client.enable_strategy(strategy_id)
        console.print(f"\n[green]✅ Strategia {strategy_id} włączona[/green]\n")

    except Exception as e:
        console.print(f"[red]❌ Błąd: {str(e)}[/red]")


@app.command()
def disable(
    strategy_id: int = typer.Argument(..., help="ID strategii"),
    api_url: str = typer.Option("http://localhost:8000", "--api")
):
    """Wyłącz strategię."""
    if typer.confirm(f"Wyłączyć strategię {strategy_id}?"):
        try:
            client.api_url = api_url
            result = client.disable_strategy(strategy_id)
            console.print(f"\n[yellow]🔴 Strategia {strategy_id} wyłączona[/yellow]\n")

        except Exception as e:
            console.print(f"[red]❌ Błąd: {str(e)}[/red]")


# ========== POZYCJE ==========

@app.command()
def positions(api_url: str = typer.Option("http://localhost:8000", "--api")):
    """Wyświetl otwarte pozycje."""
    try:
        client.api_url = api_url
        data = client.get_positions()

        if len(data['positions']) == 0:
            console.print("[yellow]ℹ️  Brak otwartych pozycji[/yellow]\n")
            return

        table = Table(title="Otwarte Pozycje")
        table.add_column("Ticket", style="cyan")
        table.add_column("Symbol", style="magenta")
        table.add_column("Typ", style="green")
        table.add_column("Rozmiar", style="blue")
        table.add_column("Cena Otwarcia", style="white")
        table.add_column("Aktualna", style="white")
        table.add_column("P&L", style="yellow")

        for pos in data['positions']:
            pnl_color = "green" if pos['profit'] > 0 else "red"
            table.add_row(
                str(pos['ticket']),
                pos['symbol'],
                pos['type'],
                f"{pos['volume']:.2f}",
                f"{pos['open_price']:.2f}",
                f"{pos['current_price']:.2f}",
                f"[{pnl_color}]${pos['profit']:.2f}[/{pnl_color}]"
            )

        console.print(table)
        console.print(f"\nTotal: {data['total']} pozycji\n")

    except Exception as e:
        console.print(f"[red]❌ Błąd: {str(e)}[/red]")


@app.command()
def close_pos(
    position_id: int = typer.Argument(..., help="ID pozycji"),
    exit_price: Optional[float] = typer.Option(None, "--price", help="Cena wyjścia"),
    api_url: str = typer.Option("http://localhost:8000", "--api")
):
    """Zamknij pozycję."""
    if typer.confirm(f"Zamknąć pozycję {position_id}?"):
        try:
            client.api_url = api_url
            result = client.close_position(position_id, exit_price)
            console.print(f"\n[green]✅ Pozycja {position_id} zamknięta[/green]")
            console.print(f"Cena: {result['exit_price']}\n")

        except Exception as e:
            console.print(f"[red]❌ Błąd: {str(e)}[/red]")


# ========== TRANSAKCJE ==========

@app.command()
def trades(
    limit: int = typer.Option(20, "--limit", help="Ilość transakcji"),
    days: int = typer.Option(30, "--days", help="Liczba dni"),
    api_url: str = typer.Option("http://localhost:8000", "--api")
):
    """Wyświetl ostatnie transakcje."""
    try:
        client.api_url = api_url
        data = client.get_trades(limit=limit, days=days)

        if len(data['trades']) == 0:
            console.print("[yellow]ℹ️  Brak transakcji[/yellow]\n")
            return

        table = Table(title=f"Ostatnie Transakcje (ostatnie {days} dni)")
        table.add_column("ID", style="cyan")
        table.add_column("Symbol", style="magenta")
        table.add_column("Typ", style="green")
        table.add_column("Wejście", style="blue")
        table.add_column("Wyjście", style="blue")
        table.add_column("P&L", style="white")
        table.add_column("Return %", style="white")
        table.add_column("Data", style="white")

        for trade in data['trades']:
            if trade['profit_loss']:
                pnl_color = "green" if trade['profit_loss'] > 0 else "red"
                pnl_text = f"[{pnl_color}]${trade['profit_loss']:.2f}[/{pnl_color}]"
                ret_text = f"[{pnl_color}]{trade['profit_pct']:.2f}%[/{pnl_color}]"
            else:
                pnl_text = "-"
                ret_text = "-"

            table.add_row(
                str(trade['id']),
                trade['symbol'],
                trade['direction'],
                f"{trade['entry_price']:.2f}",
                f"{trade['exit_price']:.2f}" if trade['exit_price'] else "-",
                pnl_text,
                ret_text,
                trade['entry_time'][:10] if trade['entry_time'] else "-"
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]❌ Błąd: {str(e)}[/red]")


# ========== RYZYKO ==========

@app.command()
def risk(api_url: str = typer.Option("http://localhost:8000", "--api")):
    """Wyświetl metryki ryzyka."""
    try:
        client.api_url = api_url
        data = client.get_risk_metrics()
        metrics = data['metrics']

        panel = Panel(
            f"""
[bold cyan]🚨 Metryki Ryzyka[/bold cyan]

Kapitał: [green]${metrics['current_equity']:,.2f}[/green]
Drawdown: {metrics['drawdown_level']}
  Current: {metrics['current_drawdown']:.2f}%
  Daily Loss: {metrics['daily_loss_pct']:.2f}%

Pozycje: {metrics['open_positions']}
  Wartość: ${metrics['total_position_value']:,.2f}
  Margin: {metrics['margin_utilization']:.2f}%
            """,
            title="[bold]Risk Metrics[/bold]",
            border_style="red" if "CRITICAL" in metrics['drawdown_level'] else "yellow"
        )

        console.print(panel)

    except Exception as e:
        console.print(f"[red]❌ Błąd: {str(e)}[/red]")


# ========== CENY I ŚWIECE ==========

@app.command()
def price(
    symbol: str = typer.Argument(..., help="Symbol"),
    api_url: str = typer.Option("http://localhost:8000", "--api")
):
    """Pobierz aktualną cenę."""
    try:
        client.api_url = api_url
        data = client.get_price(symbol)

        spread = data['spread'] * 10000  # W pips

        console.print(f"\n[cyan]{symbol}[/cyan]")
        console.print(f"  Bid: [red]{data['bid']:.5f}[/red]")
        console.print(f"  Ask: [green]{data['ask']:.5f}[/green]")
        console.print(f"  Spread: {spread:.1f} pips")
        console.print(f"  Czas: {data['timestamp']}\n")

    except Exception as e:
        console.print(f"[red]❌ Błąd: {str(e)}[/red]")


# ========== ZARZĄDZANIE RĘCZNE ==========

@app.command()
def order(
    symbol: str = typer.Argument(..., help="Symbol"),
    direction: str = typer.Argument(..., help="BUY lub SELL"),
    lot_size: float = typer.Argument(..., help="Rozmiar w lotach"),
    price: float = typer.Option(0, "--price", help="Cena (0=market)"),
    tp: float = typer.Option(0, "--tp", help="Take profit"),
    sl: float = typer.Option(0, "--sl", help="Stop loss"),
    api_url: str = typer.Option("http://localhost:8000", "--api")
):
    """Złóż ręczne zlecenie."""
    if typer.confirm(f"Złożyć zlecenie {direction} {lot_size} {symbol}?"):
        try:
            client.api_url = api_url
            result = client.place_order(symbol, direction, lot_size, price, tp, sl)

            console.print(f"\n[green]✅ Zlecenie złożone[/green]")
            console.print(f"Ticket: {result['order_ticket']}\n")

        except Exception as e:
            console.print(f"[red]❌ Błąd: {str(e)}[/red]")


# ========== HELP ==========

@app.command()
def commands():
    """Pokaż dostępne komendy."""
    help_text = """
[bold cyan]📋 Dostępne Komendy:[/bold cyan]

[bold]Status[/bold]
  status          - Sprawdź pełny status systemu
  health          - Sprawdź health check

[bold]Trading Control[/bold]
  start           - Uruchom live trading
  stop            - Zatrzymaj trading
  emergency       - 🚨 EMERGENCY STOP (zamknij wszystko)

[bold]Strategie[/bold]
  strategies      - Wyświetl strategie
  enable <id>     - Włącz strategię
  disable <id>    - Wyłącz strategię

[bold]Pozycje[/bold]
  positions       - Wyświetl otwarte pozycje
  close-pos <id>  - Zamknij pozycję

[bold]Transakcje[/bold]
  trades          - Wyświetl ostatnie transakcje

[bold]Ryzyko[/bold]
  risk            - Metryki ryzyka

[bold]Ceny[/bold]
  price <symbol>  - Aktualna cena symbolu

[bold]Zarządzanie[/bold]
  order           - Złóż ręczne zlecenie

[bold]Opcje globalne[/bold]
  --api=URL       - Adres API (default: http://localhost:8000)
    """
    console.print(help_text)


if __name__ == "__main__":
    app()
