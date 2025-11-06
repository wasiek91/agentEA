#!/usr/bin/env python3
"""Remote MT5 Helper - Place Order.
Install on VPS alongside MetaTrader5.
Usage: python3 place_order.py --symbol XAUUSD --action BUY --lots 1.0 --tp 2020 --sl 1980
"""
import sys
import json
import logging
import argparse
import MetaTrader5 as mt5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def place_order(symbol: str, action: str, lot_size: float, price: float = 0,
                take_profit: float = 0, stop_loss: float = 0, comment: str = "PM_Pro") -> dict:
    """Place order on MT5.

    Args:
        symbol: Trading symbol
        action: BUY or SELL
        lot_size: Order volume in lots
        price: Order price (0 for market)
        take_profit: Take profit level
        stop_loss: Stop loss level
        comment: Order comment

    Returns: JSON-serializable dict with order result
    """
    try:
        # Initialize MT5
        if not mt5.initialize():
            return {
                'status': 'error',
                'message': f'MT5 initialization failed: {mt5.last_error()}'
            }

        # Get current price
        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            return {
                'status': 'error',
                'message': f'Cannot get price for {symbol}'
            }

        # Determine order type and price
        if action.upper() == 'BUY':
            order_type = mt5.ORDER_TYPE_BUY
            order_price = tick.ask if price == 0 else price
        elif action.upper() == 'SELL':
            order_type = mt5.ORDER_TYPE_SELL
            order_price = tick.bid if price == 0 else price
        else:
            return {
                'status': 'error',
                'message': f'Invalid action: {action}'
            }

        # Create order request
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot_size,
            "type": order_type,
            "price": order_price,
            "sl": stop_loss if stop_loss > 0 else 0,
            "tp": take_profit if take_profit > 0 else 0,
            "deviation": 20,
            "magic": 234000,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        # Send order
        result = mt5.order_send(request)

        mt5.shutdown()

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return {
                'status': 'error',
                'message': f'Order failed: {result.comment}',
                'retcode': int(result.retcode)
            }

        return {
            'status': 'success',
            'order_ticket': int(result.order),
            'symbol': symbol,
            'action': action,
            'lot_size': lot_size,
            'price': order_price,
            'take_profit': take_profit,
            'stop_loss': stop_loss,
            'comment': comment
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            'status': 'error',
            'message': str(e)
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Place order on MT5')
    parser.add_argument('--symbol', required=True, help='Trading symbol')
    parser.add_argument('--action', required=True, help='BUY or SELL')
    parser.add_argument('--lots', type=float, required=True, help='Order size in lots')
    parser.add_argument('--price', type=float, default=0, help='Order price (0 for market)')
    parser.add_argument('--tp', type=float, default=0, help='Take profit level')
    parser.add_argument('--sl', type=float, default=0, help='Stop loss level')
    parser.add_argument('--comment', default='PM_Pro', help='Order comment')

    args = parser.parse_args()

    result = place_order(
        symbol=args.symbol,
        action=args.action,
        lot_size=args.lots,
        price=args.price,
        take_profit=args.tp,
        stop_loss=args.sl,
        comment=args.comment
    )

    print(json.dumps(result))
