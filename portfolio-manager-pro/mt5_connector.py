"""MT5 Connector - Local & Remote Support."""
import MetaTrader5 as mt5
import paramiko
from typing import Dict, List, Optional
import logging
from config import settings

logger = logging.getLogger(__name__)


class MT5Manager:
    """Manages MT5 connections (local or remote)."""

    def __init__(self):
        """Initialize MT5 Manager."""
        self.remote_enabled = settings.MT5_REMOTE_ENABLED
        self.ssh_client = None
        self.mt5_connection = None

        if self.remote_enabled:
            logger.info("🌐 Using REMOTE MT5 (VPS/Server)")
            self._connect_remote()
        else:
            logger.info("💻 Using LOCAL MT5")
            self._connect_local()

    def _connect_local(self):
        """Connect to local MT5 terminal."""
        try:
            if not mt5.initialize():
                raise Exception(f"MT5 initialization failed: {mt5.last_error()}")

            authorized = mt5.login(
                login=int(settings.MT5_ACCOUNT_LOCAL),
                password=settings.MT5_PASSWORD_LOCAL,
                server=settings.MT5_SERVER_LOCAL
            )

            if not authorized:
                raise Exception(f"MT5 login failed: {mt5.last_error()}")

            logger.info(f"✅ Connected to LOCAL MT5")
            self._log_account_info()

        except Exception as e:
            logger.error(f"❌ Local MT5 connection failed: {e}")
            raise

    def _connect_remote(self):
        """Connect to remote MT5 via SSH."""
        try:
            # SSH Connection
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if settings.MT5_REMOTE_SSH_KEY:
                self.ssh_client.connect(
                    hostname=settings.MT5_REMOTE_HOST,
                    port=settings.MT5_REMOTE_PORT,
                    username=settings.MT5_REMOTE_USER,
                    key_filename=settings.MT5_REMOTE_SSH_KEY
                )
                logger.info("✅ SSH connected via key")
            else:
                self.ssh_client.connect(
                    hostname=settings.MT5_REMOTE_HOST,
                    port=settings.MT5_REMOTE_PORT,
                    username=settings.MT5_REMOTE_USER,
                    password=settings.MT5_REMOTE_PASSWORD
                )
                logger.info("✅ SSH connected via password")

            logger.info(f"✅ Connected to REMOTE MT5 ({settings.MT5_REMOTE_HOST})")

        except Exception as e:
            logger.error(f"❌ Remote MT5 connection failed: {e}")
            raise

    def get_candles(self, symbol: str, timeframe: int, num_candles: int = 500) -> Optional[Dict]:
        """
        Get historical candles.

        Args:
            symbol: 'XAUUSD', 'NASDAQ'
            timeframe: 1, 5, 15, 60, 1440
            num_candles: number of candles

        Returns:
            DataFrame with OHLCV data or None
        """
        try:
            if self.remote_enabled:
                return self._get_candles_remote(symbol, timeframe, num_candles)
            else:
                return self._get_candles_local(symbol, timeframe, num_candles)

        except Exception as e:
            logger.error(f"❌ Failed to get candles: {e}")
            return None

    def _get_candles_local(self, symbol: str, timeframe: int, num_candles: int):
        """Get candles from local MT5."""
        timeframe_map = {
            1: mt5.TIMEFRAME_M1,
            5: mt5.TIMEFRAME_M5,
            15: mt5.TIMEFRAME_M15,
            60: mt5.TIMEFRAME_H1,
            240: mt5.TIMEFRAME_H4,
            1440: mt5.TIMEFRAME_D1
        }

        tf = timeframe_map.get(timeframe, mt5.TIMEFRAME_H1)
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, num_candles)

        if rates is None:
            return None

        import pandas as pd
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df[['time', 'open', 'high', 'low', 'close', 'tick_volume']]
        df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

        logger.info(f"✅ Got {len(df)} candles for {symbol} ({timeframe}m)")
        return df.to_dict('records')

    def _get_candles_remote(self, symbol: str, timeframe: int, num_candles: int):
        """Get candles from remote MT5 via SSH."""
        # Execute remote script to fetch candles
        script = f"""
        import MetaTrader5 as mt5
        mt5.initialize()
        # ... fetch candles logic ...
        """

        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(
                f"python3 {settings.MT5_REMOTE_PATH}/get_candles.py {symbol} {timeframe} {num_candles}"
            )

            output = stdout.read().decode()
            if stderr:
                logger.error(f"Remote error: {stderr.read().decode()}")
                return None

            import json
            return json.loads(output)

        except Exception as e:
            logger.error(f"❌ Remote candle fetch failed: {e}")
            return None

    def get_current_price(self, symbol: str) -> Optional[Dict]:
        """Get current bid/ask price."""
        try:
            if self.remote_enabled:
                return self._get_price_remote(symbol)
            else:
                return self._get_price_local(symbol)

        except Exception as e:
            logger.error(f"❌ Failed to get price: {e}")
            return None

    def _get_price_local(self, symbol: str):
        """Get price from local MT5."""
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return None

        return {
            'symbol': symbol,
            'bid': tick.bid,
            'ask': tick.ask,
            'time': tick.time
        }

    def _get_price_remote(self, symbol: str):
        """Get price from remote MT5."""
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(
                f"python3 {settings.MT5_REMOTE_PATH}/get_price.py {symbol}"
            )
            output = stdout.read().decode()
            import json
            return json.loads(output)

        except Exception as e:
            logger.error(f"❌ Remote price fetch failed: {e}")
            return None

    def place_order(self, symbol: str, action: str, lot_size: float,
                   price: float = 0, take_profit: float = 0,
                   stop_loss: float = 0, comment: str = "PM_Pro") -> Optional[int]:
        """Place an order."""
        try:
            if self.remote_enabled:
                return self._place_order_remote(symbol, action, lot_size, price, take_profit, stop_loss, comment)
            else:
                return self._place_order_local(symbol, action, lot_size, price, take_profit, stop_loss, comment)

        except Exception as e:
            logger.error(f"❌ Failed to place order: {e}")
            return None

    def _place_order_local(self, symbol: str, action: str, lot_size: float,
                          price: float, take_profit: float,
                          stop_loss: float, comment: str):
        """Place order on local MT5."""
        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            return None

        action_type = mt5.ORDER_TYPE_BUY if action.upper() == 'BUY' else mt5.ORDER_TYPE_SELL
        price = tick.ask if action.upper() == 'BUY' else tick.bid if price == 0 else price

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot_size,
            "type": action_type,
            "price": price,
            "sl": stop_loss if stop_loss > 0 else 0,
            "tp": take_profit if take_profit > 0 else 0,
            "deviation": 20,
            "magic": 234000,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"❌ Order failed: {result.comment}")
            return None

        logger.info(f"✅ Order {action} {lot_size} {symbol} @ {price}")
        return result.order

    def _place_order_remote(self, symbol: str, action: str, lot_size: float,
                           price: float, take_profit: float,
                           stop_loss: float, comment: str):
        """Place order on remote MT5."""
        try:
            cmd = f"""
python3 {settings.MT5_REMOTE_PATH}/place_order.py \\
    --symbol {symbol} --action {action} --lots {lot_size} \\
    --tp {take_profit} --sl {stop_loss} --comment {comment}
            """

            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
            output = stdout.read().decode()

            import json
            result = json.loads(output)
            return result.get('order_ticket')

        except Exception as e:
            logger.error(f"❌ Remote order placement failed: {e}")
            return None

    def get_open_positions(self, symbol: str = None) -> List[Dict]:
        """Get all open positions."""
        try:
            if self.remote_enabled:
                return self._get_positions_remote(symbol)
            else:
                return self._get_positions_local(symbol)

        except Exception as e:
            logger.error(f"❌ Failed to get positions: {e}")
            return []

    def _get_positions_local(self, symbol: str = None):
        """Get positions from local MT5."""
        positions = mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()

        if not positions:
            return []

        result = []
        for pos in positions:
            result.append({
                'ticket': pos.ticket,
                'symbol': pos.symbol,
                'type': 'BUY' if pos.type == 0 else 'SELL',
                'volume': pos.volume,
                'open_price': pos.price_open,
                'current_price': pos.price_current,
                'profit': pos.profit,
                'open_time': pos.time
            })

        return result

    def _get_positions_remote(self, symbol: str = None):
        """Get positions from remote MT5."""
        try:
            cmd = f"python3 {settings.MT5_REMOTE_PATH}/get_positions.py"
            if symbol:
                cmd += f" --symbol {symbol}"

            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
            output = stdout.read().decode()

            import json
            return json.loads(output)

        except Exception as e:
            logger.error(f"❌ Remote positions fetch failed: {e}")
            return []

    def get_account_balance(self) -> Dict:
        """Get account balance and equity."""
        try:
            if self.remote_enabled:
                return self._get_balance_remote()
            else:
                return self._get_balance_local()

        except Exception as e:
            logger.error(f"❌ Failed to get balance: {e}")
            return {}

    def _get_balance_local(self):
        """Get balance from local MT5."""
        account_info = mt5.account_info()
        return {
            'balance': account_info.balance,
            'equity': account_info.equity,
            'margin_free': account_info.margin_free,
            'margin_used': account_info.margin,
            'margin_level': account_info.margin_level
        }

    def _get_balance_remote(self):
        """Get balance from remote MT5."""
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(
                f"python3 {settings.MT5_REMOTE_PATH}/get_balance.py"
            )
            output = stdout.read().decode()

            import json
            return json.loads(output)

        except Exception as e:
            logger.error(f"❌ Remote balance fetch failed: {e}")
            return {}

    def _log_account_info(self):
        """Log account information."""
        balance = self.get_account_balance()
        if balance:
            logger.info(f"  Balance: ${balance.get('balance', 0):,.2f}")
            logger.info(f"  Equity: ${balance.get('equity', 0):,.2f}")
            logger.info(f"  Free Margin: ${balance.get('margin_free', 0):,.2f}")

    def disconnect(self):
        """Disconnect from MT5."""
        try:
            if self.remote_enabled and self.ssh_client:
                self.ssh_client.close()
                logger.info("✅ Disconnected from remote MT5")
            elif not self.remote_enabled:
                mt5.shutdown()
                logger.info("✅ Disconnected from local MT5")
        except Exception as e:
            logger.error(f"❌ Disconnection failed: {e}")


if __name__ == "__main__":
    mt5_mgr = MT5Manager()
    print(mt5_mgr.get_account_balance())
    mt5_mgr.disconnect()
