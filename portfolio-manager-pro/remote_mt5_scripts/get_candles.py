#!/usr/bin/env python3
"""Remote MT5 Helper - Fetch Candles.
Install on VPS alongside MetaTrader5.
Usage: python3 get_candles.py XAUUSD 60 500
"""
import sys
import json
import logging
from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_candles(symbol: str, timeframe: int, num_candles: int) -> dict:
    """Fetch historical candles from MT5.

    Args:
        symbol: Trading symbol (XAUUSD, NASDAQ, etc.)
        timeframe: Timeframe in minutes (1, 5, 15, 60, 1440)
        num_candles: Number of candles to fetch

    Returns: JSON-serializable dict with candle data
    """
    try:
        # Initialize MT5
        if not mt5.initialize():
            return {
                'status': 'error',
                'message': f'MT5 initialization failed: {mt5.last_error()}'
            }

        # Map timeframe to MT5 constants
        timeframe_map = {
            1: mt5.TIMEFRAME_M1,
            5: mt5.TIMEFRAME_M5,
            15: mt5.TIMEFRAME_M15,
            60: mt5.TIMEFRAME_H1,
            240: mt5.TIMEFRAME_H4,
            1440: mt5.TIMEFRAME_D1
        }

        tf = timeframe_map.get(timeframe, mt5.TIMEFRAME_H1)

        # Fetch candles
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, num_candles)

        if rates is None:
            return {
                'status': 'error',
                'message': f'Failed to get candles for {symbol}: {mt5.last_error()}'
            }

        # Convert to DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')

        # Format for JSON
        candles = []
        for _, row in df.iterrows():
            candles.append({
                'timestamp': row['time'].isoformat(),
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'volume': int(row['tick_volume'])
            })

        mt5.shutdown()

        return {
            'status': 'success',
            'symbol': symbol,
            'timeframe': timeframe,
            'candles': candles,
            'count': len(candles)
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            'status': 'error',
            'message': str(e)
        }


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({
            'status': 'error',
            'message': 'Usage: get_candles.py SYMBOL TIMEFRAME NUM_CANDLES'
        }))
        sys.exit(1)

    symbol = sys.argv[1]
    timeframe = int(sys.argv[2])
    num_candles = int(sys.argv[3])

    result = get_candles(symbol, timeframe, num_candles)
    print(json.dumps(result))
