"""Real-time Dashboard - Portfolio Monitoring UI."""
import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List
from database import Database
from risk_manager import RiskManager
from config import settings

logger = logging.getLogger(__name__)


class PortfolioDashboard:
    """Real-time portfolio dashboard using Plotly-Dash."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8050, debug: bool = False):
        """Initialize dashboard.

        Args:
            host: Server host
            port: Server port
            debug: Debug mode
        """
        self.host = host
        self.port = port
        self.debug = debug
        self.db = Database()
        self.risk_mgr = RiskManager()

        # Initialize Dash app
        self.app = dash.Dash(__name__)
        self.app.title = "Portfolio Manager Pro - Dashboard"

        # Build layout
        self._build_layout()
        self._setup_callbacks()

    def _build_layout(self):
        """Build dashboard layout."""
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1("📊 Portfolio Manager Pro - Real-time Dashboard", className="header-title"),
                html.Div([
                    html.Span(f"Last Updated: ", style={'fontWeight': 'bold'}),
                    html.Span(id='last-updated', children=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                ], style={'fontSize': '14px', 'color': '#666'})
            ], className="header", style={
                'padding': '20px',
                'backgroundColor': '#f8f9fa',
                'borderBottom': '2px solid #007bff'
            }),

            # Auto-refresh interval
            dcc.Interval(id='interval-update', interval=5000, n_intervals=0),

            # Main content
            html.Div([
                # Row 1: Key Metrics
                html.Div([
                    # Equity Card
                    html.Div([
                        html.H4("Current Equity", style={'color': '#666'}),
                        html.H2(id='equity-value', children="$100,000.00", style={'color': '#28a745'}),
                        html.P(id='equity-change', children="+5.2%", style={'color': '#28a745'})
                    ], className="metric-card", style=self._get_card_style()),

                    # Drawdown Card
                    html.Div([
                        html.H4("Current Drawdown", style={'color': '#666'}),
                        html.H2(id='drawdown-value', children="2.5%", style={'color': '#ffc107'}),
                        html.P(id='drawdown-level', children="🟢 SAFE", style={'color': '#ffc107'})
                    ], className="metric-card", style=self._get_card_style()),

                    # Win Rate Card
                    html.Div([
                        html.H4("Win Rate", style={'color': '#666'}),
                        html.H2(id='win-rate-value', children="65%", style={'color': '#17a2b8'}),
                        html.P(id='win-rate-trades', children="26/40 trades", style={'color': '#17a2b8'})
                    ], className="metric-card", style=self._get_card_style()),

                    # Active Strategies Card
                    html.Div([
                        html.H4("Active Strategies", style={'color': '#666'}),
                        html.H2(id='strategy-count', children="3", style={'color': '#6f42c1'}),
                        html.P(id='strategy-profit', children="Total Profit: $5,200", style={'color': '#6f42c1'})
                    ], className="metric-card", style=self._get_card_style()),
                ], style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(4, 1fr)',
                    'gap': '20px',
                    'marginBottom': '30px'
                }),

                # Row 2: Charts
                html.Div([
                    # Equity Curve
                    html.Div([
                        dcc.Graph(id='equity-chart')
                    ], style={'flex': '1', 'minWidth': '45%'}),

                    # Drawdown Gauge
                    html.Div([
                        dcc.Graph(id='drawdown-gauge')
                    ], style={'flex': '1', 'minWidth': '45%'}),
                ], style={
                    'display': 'flex',
                    'gap': '20px',
                    'marginBottom': '30px'
                }),

                # Row 3: Strategy Performance
                html.Div([
                    html.H3("📈 Strategy Performance", style={'marginBottom': '15px'}),
                    dcc.Graph(id='strategy-performance-table')
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
                }),

                # Row 4: Recent Trades
                html.Div([
                    html.H3("📋 Recent Trades", style={'marginBottom': '15px'}),
                    html.Div(id='trades-table')
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
                }),

                # Row 5: Risk Metrics
                html.Div([
                    html.H3("🚨 Risk Metrics", style={'marginBottom': '15px'}),
                    html.Div([
                        html.Div(id='risk-gauge-1', style={'flex': '1'}),
                        html.Div(id='risk-gauge-2', style={'flex': '1'}),
                        html.Div(id='risk-gauge-3', style={'flex': '1'}),
                    ], style={'display': 'flex', 'gap': '20px'})
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
                })

            ], style={
                'padding': '20px',
                'maxWidth': '1600px',
                'margin': '0 auto'
            })

        ], style={
            'fontFamily': 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
            'backgroundColor': '#f5f5f5',
            'minHeight': '100vh'
        })

    def _setup_callbacks(self):
        """Setup dashboard callbacks."""

        @self.app.callback(
            [
                Output('equity-value', 'children'),
                Output('equity-change', 'children'),
                Output('drawdown-value', 'children'),
                Output('drawdown-level', 'children'),
                Output('equity-chart', 'figure'),
                Output('drawdown-gauge', 'figure'),
                Output('win-rate-value', 'children'),
                Output('win-rate-trades', 'children'),
                Output('strategy-count', 'children'),
                Output('strategy-profit', 'children'),
                Output('strategy-performance-table', 'children'),
                Output('trades-table', 'children'),
                Output('last-updated', 'children'),
            ],
            [Input('interval-update', 'n_intervals')]
        )
        def update_dashboard(n):
            """Update all dashboard components."""
            try:
                # Get current metrics
                metrics = self.risk_mgr.get_risk_metrics()
                equity = metrics.get('current_equity', settings.INITIAL_CAPITAL)
                drawdown = metrics.get('current_drawdown', 0)
                drawdown_level = metrics.get('drawdown_level', '✅ SAFE')

                # Calculate equity change
                equity_change_pct = ((equity - settings.INITIAL_CAPITAL) / settings.INITIAL_CAPITAL) * 100

                # Get portfolio history
                history = self.db.get_portfolio_history(days=30)

                # Get recent trades
                trades = self.db.fetch_df(
                    "SELECT * FROM trades WHERE status = 'CLOSED' ORDER BY exit_time DESC LIMIT 50"
                )

                # Get strategies
                strategies = self.db.get_active_strategies()

                # Build components
                equity_figure = self._build_equity_chart(history)
                drawdown_figure = self._build_drawdown_gauge(drawdown)
                performance_table = self._build_performance_table(strategies)
                trades_table = self._build_trades_table(trades)

                # Calculate win rate
                if len(trades) > 0:
                    winning_trades = len(trades[trades['profit_loss'] > 0])
                    total_trades = len(trades)
                    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
                    win_rate_text = f"{int(winning_trades)}/{total_trades} trades"
                else:
                    win_rate = 0
                    win_rate_text = "0/0 trades"

                # Strategy stats
                total_profit = trades['profit_loss'].sum() if len(trades) > 0 else 0

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                return (
                    f"${equity:,.2f}",
                    f"{equity_change_pct:+.2f}%",
                    f"{drawdown:.2f}%",
                    drawdown_level,
                    equity_figure,
                    drawdown_figure,
                    f"{int(win_rate)}%",
                    win_rate_text,
                    str(len(strategies)),
                    f"Total Profit: ${total_profit:,.2f}",
                    performance_table,
                    trades_table,
                    timestamp
                )

            except Exception as e:
                logger.error(f"❌ Dashboard update failed: {e}")
                return ("ERROR", "ERROR", "ERROR", "ERROR", {}, {}, "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def _build_equity_chart(self, history: pd.DataFrame) -> go.Figure:
        """Build equity curve chart."""
        fig = go.Figure()

        if len(history) > 0:
            fig.add_trace(go.Scatter(
                x=history['date'],
                y=history['equity'],
                mode='lines+markers',
                name='Equity',
                line=dict(color='#007bff', width=2),
                fill='tozeroy'
            ))

        fig.update_layout(
            title="Portfolio Equity Curve (Last 30 Days)",
            xaxis_title="Date",
            yaxis_title="Equity ($)",
            hovermode='x unified',
            height=400,
            template='plotly_white'
        )

        return fig

    def _build_drawdown_gauge(self, drawdown: float) -> go.Figure:
        """Build drawdown gauge chart."""
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=drawdown,
            title={'text': "Current Drawdown (%)"},
            gauge={
                'axis': {'range': [0, 20]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 4], 'color': "#d4edda"},
                    {'range': [4, 8], 'color': "#fff3cd"},
                    {'range': [8, 12], 'color': "#f8d7da"},
                    {'range': [12, 20], 'color': "#f5c6cb"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 12
                }
            }
        ))

        fig.update_layout(height=400, template='plotly_white')
        return fig

    def _build_performance_table(self, strategies: pd.DataFrame) -> html.Div:
        """Build strategy performance table."""
        if len(strategies) == 0:
            return html.P("No active strategies")

        rows = []
        for idx, strategy in strategies.iterrows():
            rows.append(html.Tr([
                html.Td(strategy['name'], style={'padding': '10px'}),
                html.Td(strategy['type'], style={'padding': '10px'}),
                html.Td(f"{strategy.get('allocation', 0):.1f}%", style={'padding': '10px'}),
                html.Td(f"{strategy.get('performance_score', 0):.2f}", style={'padding': '10px'}),
            ]))

        return html.Table([
            html.Thead(html.Tr([
                html.Th("Strategy", style={'padding': '10px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd'}),
                html.Th("Type", style={'padding': '10px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd'}),
                html.Th("Allocation", style={'padding': '10px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd'}),
                html.Th("Score", style={'padding': '10px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd'}),
            ])),
            html.Tbody(rows)
        ], style={'width': '100%', 'borderCollapse': 'collapse'})

    def _build_trades_table(self, trades: pd.DataFrame) -> html.Div:
        """Build recent trades table."""
        if len(trades) == 0:
            return html.P("No trades yet")

        rows = []
        for idx, trade in trades.head(20).iterrows():
            profit_color = '#28a745' if trade['profit_loss'] > 0 else '#dc3545'
            rows.append(html.Tr([
                html.Td(str(trade['entry_time'])[:10], style={'padding': '8px', 'fontSize': '12px'}),
                html.Td(trade['symbol'], style={'padding': '8px', 'fontSize': '12px'}),
                html.Td(trade['direction'], style={'padding': '8px', 'fontSize': '12px'}),
                html.Td(f"{trade['entry_price']:.2f}", style={'padding': '8px', 'fontSize': '12px'}),
                html.Td(f"{trade['exit_price']:.2f}", style={'padding': '8px', 'fontSize': '12px'}),
                html.Td(f"${trade['profit_loss']:.2f}", style={'padding': '8px', 'fontSize': '12px', 'color': profit_color, 'fontWeight': 'bold'}),
                html.Td(f"{trade.get('profit_pct', 0):.2f}%", style={'padding': '8px', 'fontSize': '12px', 'color': profit_color}),
            ]))

        return html.Table([
            html.Thead(html.Tr([
                html.Th("Date", style={'padding': '8px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd', 'fontSize': '12px'}),
                html.Th("Symbol", style={'padding': '8px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd', 'fontSize': '12px'}),
                html.Th("Direction", style={'padding': '8px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd', 'fontSize': '12px'}),
                html.Th("Entry", style={'padding': '8px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd', 'fontSize': '12px'}),
                html.Th("Exit", style={'padding': '8px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd', 'fontSize': '12px'}),
                html.Th("P&L", style={'padding': '8px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd', 'fontSize': '12px'}),
                html.Th("Return %", style={'padding': '8px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd', 'fontSize': '12px'}),
            ])),
            html.Tbody(rows)
        ], style={'width': '100%', 'borderCollapse': 'collapse', 'fontSize': '12px'})

    @staticmethod
    def _get_card_style() -> Dict:
        """Get metric card styling."""
        return {
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'textAlign': 'center'
        }

    def run(self):
        """Start dashboard server."""
        logger.info(f"🌐 Dashboard running at http://{self.host}:{self.port}")
        self.app.run_server(host=self.host, port=self.port, debug=self.debug)


class AlertManager:
    """Manage alerts (Telegram, Email)."""

    def __init__(self):
        """Initialize alert manager."""
        self.db = Database()

    def send_telegram_alert(self, chat_id: str, message: str):
        """Send Telegram alert.

        Args:
            chat_id: Telegram chat ID
            message: Alert message
        """
        try:
            import requests
            token = settings.TELEGRAM_BOT_TOKEN
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, data={'chat_id': chat_id, 'text': message})
            logger.info(f"✅ Telegram alert sent: {message[:50]}...")
        except Exception as e:
            logger.error(f"❌ Telegram alert failed: {e}")

    def send_email_alert(self, recipient: str, subject: str, body: str):
        """Send email alert.

        Args:
            recipient: Email recipient
            subject: Email subject
            body: Email body
        """
        try:
            import smtplib
            from email.mime.text import MIMEText

            # Configure email settings
            sender = settings.EMAIL_SENDER
            password = settings.EMAIL_PASSWORD

            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = recipient

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender, password)
                server.sendmail(sender, recipient, msg.as_string())

            logger.info(f"✅ Email alert sent to {recipient}")
        except Exception as e:
            logger.error(f"❌ Email alert failed: {e}")

    def alert_on_drawdown(self, drawdown: float, threshold: float, recipients: List[str]):
        """Alert when drawdown exceeds threshold.

        Args:
            drawdown: Current drawdown percentage
            threshold: Drawdown threshold
            recipients: List of recipient emails or chat IDs
        """
        if drawdown > threshold:
            message = f"⚠️  ALERT: Drawdown exceeded {threshold}%! Current: {drawdown:.2f}%"
            for recipient in recipients:
                self.send_telegram_alert(recipient, message)

    def alert_on_trade_signal(self, signal: str, symbol: str, confidence: float):
        """Alert on trade signal.

        Args:
            signal: Trading signal (BUY/SELL)
            symbol: Trading symbol
            confidence: Signal confidence
        """
        message = f"📊 Signal: {signal} {symbol} (Confidence: {confidence:.1%})"
        # Send to configured recipients
        if hasattr(settings, 'ALERT_RECIPIENTS'):
            for recipient in settings.ALERT_RECIPIENTS:
                self.send_telegram_alert(recipient, message)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Create and run dashboard
    dashboard = PortfolioDashboard(host="127.0.0.1", port=8050, debug=True)
    dashboard.run()
