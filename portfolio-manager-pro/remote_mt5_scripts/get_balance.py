#!/usr/bin/env python3
"""Remote MT5 Helper - Get Account Balance.
Install on VPS alongside MetaTrader5.
Usage: python3 get_balance.py
"""
import sys
import json
import logging
from datetime import datetime
import MetaTrader5 as mt5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_balance() -> dict:
    """Get account balance and equity from MT5.

    Returns: JSON-serializable dict with account info
    """
    try:
        # Initialize MT5
        if not mt5.initialize():
            return {
                'status': 'error',
                'message': f'MT5 initialization failed: {mt5.last_error()}'
            }

        # Get account info
        account_info = mt5.account_info()

        if account_info is None:
            return {
                'status': 'error',
                'message': f'Failed to get account info: {mt5.last_error()}'
            }

        mt5.shutdown()

        return {
            'status': 'success',
            'login': int(account_info.login),
            'balance': float(account_info.balance),
            'equity': float(account_info.equity),
            'margin': float(account_info.margin),
            'margin_free': float(account_info.margin_free),
            'margin_level': float(account_info.margin_level),
            'profit': float(account_info.profit),
            'credit': float(account_info.credit),
            'leverage': int(account_info.leverage),
            'currency': account_info.currency,
            'server': account_info.server,
            'company': account_info.company,
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            'status': 'error',
            'message': str(e)
        }


if __name__ == "__main__":
    result = get_balance()
    print(json.dumps(result))
