#!/usr/bin/env python3
"""Remote MT5 Helper - Fetch Current Price.
Install on VPS alongside MetaTrader5.
Usage: python3 get_price.py XAUUSD
"""
import sys
import json
import logging
from datetime import datetime
import MetaTrader5 as mt5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_price(symbol: str) -> dict:
    """Fetch current bid/ask price from MT5.

    Args:
        symbol: Trading symbol

    Returns: JSON-serializable dict with price data
    """
    try:
        # Initialize MT5
        if not mt5.initialize():
            return {
                'status': 'error',
                'message': f'MT5 initialization failed: {mt5.last_error()}'
            }

        # Get tick info
        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            return {
                'status': 'error',
                'message': f'Failed to get price for {symbol}: {mt5.last_error()}'
            }

        mt5.shutdown()

        return {
            'status': 'success',
            'symbol': symbol,
            'bid': float(tick.bid),
            'ask': float(tick.ask),
            'time': int(tick.time),
            'timestamp': datetime.fromtimestamp(tick.time).isoformat()
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            'status': 'error',
            'message': str(e)
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            'status': 'error',
            'message': 'Usage: get_price.py SYMBOL'
        }))
        sys.exit(1)

    symbol = sys.argv[1]
    result = get_price(symbol)
    print(json.dumps(result))
