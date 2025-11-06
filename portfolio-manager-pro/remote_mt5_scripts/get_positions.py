#!/usr/bin/env python3
"""Remote MT5 Helper - Get Open Positions.
Install on VPS alongside MetaTrader5.
Usage: python3 get_positions.py [--symbol XAUUSD]
"""
import sys
import json
import logging
import argparse
from datetime import datetime
import MetaTrader5 as mt5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_positions(symbol: str = None) -> dict:
    """Get open positions from MT5.

    Args:
        symbol: Filter by symbol (optional)

    Returns: JSON-serializable dict with positions data
    """
    try:
        # Initialize MT5
        if not mt5.initialize():
            return {
                'status': 'error',
                'message': f'MT5 initialization failed: {mt5.last_error()}'
            }

        # Get positions
        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        else:
            positions = mt5.positions_get()

        if not positions:
            mt5.shutdown()
            return {
                'status': 'success',
                'positions': [],
                'count': 0
            }

        # Format positions
        formatted_positions = []
        for pos in positions:
            formatted_positions.append({
                'ticket': int(pos.ticket),
                'symbol': pos.symbol,
                'type': 'BUY' if pos.type == 0 else 'SELL',
                'volume': float(pos.volume),
                'price_open': float(pos.price_open),
                'price_current': float(pos.price_current),
                'sl': float(pos.sl),
                'tp': float(pos.tp),
                'profit': float(pos.profit),
                'comment': pos.comment,
                'time': int(pos.time),
                'time_update': int(pos.time_update)
            })

        mt5.shutdown()

        return {
            'status': 'success',
            'positions': formatted_positions,
            'count': len(formatted_positions),
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            'status': 'error',
            'message': str(e)
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get open positions from MT5')
    parser.add_argument('--symbol', help='Filter by symbol')

    args = parser.parse_args()

    result = get_positions(symbol=args.symbol)
    print(json.dumps(result))
