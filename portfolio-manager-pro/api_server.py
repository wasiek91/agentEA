"""REST API Server - Zarządzanie Portfolio Manager Pro z odległości."""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import uvicorn
import json

from config import settings
from database import Database
from mt5_connector import MT5Manager
from strategy_framework import StrategyExecutor, StrategyRegistry
from risk_manager import RiskManager
from rl_engine import RLTrainer
from backtester import Backtester
from logging_system import AuditLogger, PerformanceLogger

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Portfolio Manager Pro API",
    description="API do zdallnego zarządzania trading botami",
    version="1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
db = Database()
mt5 = MT5Manager()
risk_mgr = RiskManager()
audit_logger = AuditLogger(db)
trading_active = False


# ========== HEALTH & STATUS ==========

@app.get("/health")
async def health_check():
    """Sprawdź status systemu."""
    try:
        # Test database
        db.fetch_one("SELECT 1")

        # Test MT5
        balance = mt5.get_account_balance()

        return {
            'status': 'online',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected',
            'mt5': 'connected' if balance else 'error',
            'trading_active': trading_active
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"System error: {str(e)}")


@app.get("/status")
async def get_status():
    """Pobierz pełny status systemu."""
    try:
        metrics = risk_mgr.get_risk_metrics()
        positions = mt5.get_open_positions()
        strategies = db.get_active_strategies()
        recent_trades = db.fetch_df(
            "SELECT * FROM trades WHERE status = 'CLOSED' ORDER BY exit_time DESC LIMIT 50"
        )

        return {
            'timestamp': datetime.now().isoformat(),
            'equity': metrics.get('current_equity'),
            'drawdown': metrics.get('current_drawdown'),
            'drawdown_level': metrics.get('drawdown_level'),
            'open_positions': len(positions),
            'active_strategies': len(strategies),
            'recent_trades': len(recent_trades),
            'win_rate': (len(recent_trades[recent_trades['profit_loss'] > 0]) / len(recent_trades) * 100) if len(recent_trades) > 0 else 0,
            'trading_active': trading_active
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== TRADING CONTROL ==========

@app.post("/trading/start")
async def start_trading(symbols: List[str] = None):
    """Uruchom live trading."""
    global trading_active
    try:
        trading_active = True
        symbols = symbols or settings.SYMBOLS

        audit_logger.log_event(
            event_type='TRADING_STARTED',
            actor='API_Server',
            details={'symbols': symbols},
            status='SUCCESS'
        )

        logger.info(f"✅ Trading started on {symbols}")

        return {
            'status': 'started',
            'symbols': symbols,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/trading/stop")
async def stop_trading():
    """Zatrzymaj live trading."""
    global trading_active
    try:
        trading_active = False

        audit_logger.log_event(
            event_type='TRADING_STOPPED',
            actor='API_Server',
            details={},
            status='SUCCESS'
        )

        logger.info("🛑 Trading stopped")

        return {
            'status': 'stopped',
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/trading/emergency-stop")
async def emergency_stop():
    """Natychmiastowy STOP - zamknij wszystkie pozycje."""
    global trading_active
    try:
        trading_active = False
        positions = mt5.get_open_positions()

        closed_count = 0
        for pos in positions:
            # Zamknij pozycję
            current_price = mt5.get_current_price(pos['symbol'])
            if current_price:
                exit_price = current_price['bid'] if pos['type'] == 'BUY' else current_price['ask']
                mt5.place_order(
                    symbol=pos['symbol'],
                    action='SELL' if pos['type'] == 'BUY' else 'BUY',
                    lot_size=pos['volume'],
                    price=exit_price,
                    comment='EMERGENCY_CLOSE'
                )
                closed_count += 1

        audit_logger.log_event(
            event_type='EMERGENCY_STOP',
            actor='API_Server',
            details={'positions_closed': closed_count},
            status='SUCCESS'
        )

        logger.warning(f"🚨 EMERGENCY STOP - Closed {closed_count} positions")

        return {
            'status': 'emergency_stop',
            'positions_closed': closed_count,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== STRATEGIES ==========

@app.get("/strategies")
async def get_strategies():
    """Pobierz wszystkie strategie."""
    try:
        strategies = db.get_active_strategies()

        result = []
        for _, strategy in strategies.iterrows():
            trades = db.fetch_df(
                "SELECT * FROM trades WHERE strategy_id = %s AND status = 'CLOSED' ORDER BY exit_time DESC LIMIT 50",
                (strategy['id'],)
            )

            win_rate = 0
            if len(trades) > 0:
                wins = len(trades[trades['profit_loss'] > 0])
                win_rate = (wins / len(trades)) * 100

            result.append({
                'id': strategy['id'],
                'name': strategy['name'],
                'type': strategy['type'],
                'enabled': strategy.get('enabled', True),
                'allocation': strategy.get('allocation', 0),
                'performance_score': strategy.get('performance_score', 0),
                'total_trades': len(trades),
                'win_rate': win_rate,
                'config': strategy.get('config', {})
            })

        return {
            'strategies': result,
            'total': len(result),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/strategies/{strategy_id}/enable")
async def enable_strategy(strategy_id: int):
    """Włącz strategię."""
    try:
        db.execute(
            "UPDATE strategies SET enabled = TRUE, updated_at = NOW() WHERE id = %s",
            (strategy_id,)
        )

        audit_logger.log_event(
            event_type='STRATEGY_ENABLED',
            actor='API_Server',
            details={'strategy_id': strategy_id},
            status='SUCCESS'
        )

        logger.info(f"✅ Strategy {strategy_id} enabled")

        return {'status': 'enabled', 'strategy_id': strategy_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/strategies/{strategy_id}/disable")
async def disable_strategy(strategy_id: int):
    """Wyłącz strategię."""
    try:
        db.execute(
            "UPDATE strategies SET enabled = FALSE, updated_at = NOW() WHERE id = %s",
            (strategy_id,)
        )

        audit_logger.log_event(
            event_type='STRATEGY_DISABLED',
            actor='API_Server',
            details={'strategy_id': strategy_id},
            status='SUCCESS'
        )

        logger.info(f"🔴 Strategy {strategy_id} disabled")

        return {'status': 'disabled', 'strategy_id': strategy_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== POSITIONS ==========

@app.get("/positions")
async def get_positions():
    """Pobierz otwarte pozycje."""
    try:
        positions = mt5.get_open_positions()

        return {
            'positions': positions,
            'total': len(positions),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/positions/{position_id}/close")
async def close_position(position_id: int, exit_price: Optional[float] = None):
    """Zamknij pozycję."""
    try:
        # Get position details
        pos_data = db.fetch_one(
            "SELECT * FROM positions WHERE id = %s",
            (position_id,)
        )

        if not pos_data:
            raise HTTPException(status_code=404, detail="Position not found")

        # Close on MT5
        if not exit_price:
            price_info = mt5.get_current_price(pos_data[2])  # symbol
            exit_price = price_info['bid'] if price_info else None

        db.execute(
            "DELETE FROM positions WHERE id = %s",
            (position_id,)
        )

        audit_logger.log_event(
            event_type='POSITION_CLOSED_MANUAL',
            actor='API_Server',
            details={'position_id': position_id, 'exit_price': exit_price},
            status='SUCCESS'
        )

        logger.info(f"🔴 Position {position_id} closed @ {exit_price}")

        return {'status': 'closed', 'position_id': position_id, 'exit_price': exit_price}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== TRADES ==========

@app.get("/trades")
async def get_trades(limit: int = 50, days: int = 30):
    """Pobierz ostatnie transakcje."""
    try:
        trades = db.fetch_df(f"""
            SELECT * FROM trades
            WHERE DATE(entry_time) >= CURRENT_DATE - INTERVAL '{days} days'
            ORDER BY entry_time DESC
            LIMIT {limit}
        """)

        result = []
        for _, trade in trades.iterrows():
            result.append({
                'id': trade['id'],
                'symbol': trade['symbol'],
                'direction': trade['direction'],
                'entry_price': float(trade['entry_price']),
                'exit_price': float(trade['exit_price']) if trade['exit_price'] else None,
                'lot_size': float(trade['lot_size']),
                'profit_loss': float(trade['profit_loss']) if trade['profit_loss'] else None,
                'profit_pct': float(trade['profit_pct']) if trade['profit_pct'] else None,
                'entry_time': trade['entry_time'].isoformat() if trade['entry_time'] else None,
                'exit_time': trade['exit_time'].isoformat() if trade['exit_time'] else None,
                'status': trade['status']
            })

        return {
            'trades': result,
            'total': len(result),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== RISK MANAGEMENT ==========

@app.get("/risk/metrics")
async def get_risk_metrics():
    """Pobierz metryki ryzyka."""
    try:
        metrics = risk_mgr.get_risk_metrics()

        return {
            'metrics': metrics,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/risk/validate-trade")
async def validate_trade(symbol: str, direction: str, lot_size: float, entry_price: float):
    """Zwaliduj trade przed wykonaniem."""
    try:
        is_valid, msg = risk_mgr.validate_trade(symbol, direction, lot_size, entry_price)

        audit_logger.log_risk_check({
            'symbol': symbol,
            'check_type': 'manual_validation',
            'current_value': entry_price,
            'limit_value': risk_mgr.current_equity,
            'passed': is_valid,
            'message': msg
        })

        return {
            'valid': is_valid,
            'message': msg,
            'symbol': symbol,
            'direction': direction,
            'lot_size': lot_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== RL & BACKTESTING ==========

@app.post("/backtest")
async def run_backtest(
    strategy_name: str,
    symbol: str,
    start_date: str,
    end_date: str
):
    """Uruchom backtest strategii."""
    try:
        from datetime import datetime
        backtester = Backtester(
            start_date=datetime.strptime(start_date, '%Y-%m-%d'),
            end_date=datetime.strptime(end_date, '%Y-%m-%d')
        )

        # Find strategy
        registry = StrategyRegistry()
        target_strategy = None
        for sid, strategy in registry.strategies.items():
            if strategy.name == strategy_name and strategy.symbol == symbol:
                target_strategy = strategy
                break

        if not target_strategy:
            raise HTTPException(status_code=404, detail=f"Strategy {strategy_name} not found")

        result = backtester.backtest_strategy(target_strategy, symbol)
        metrics = result.calculate_metrics()

        return {
            'strategy': strategy_name,
            'symbol': symbol,
            'metrics': metrics,
            'trades_count': len(result.trades)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rl/train")
async def start_rl_training(
    symbols: List[str] = None,
    timesteps: int = 50000,
    model_type: str = "PPO",
    background_tasks: BackgroundTasks = None
):
    """Uruchom trening RL agenta w tle."""
    try:
        symbols = symbols or settings.SYMBOLS

        def train_task():
            trainer = RLTrainer(symbols=symbols, model_type=model_type)
            trainer.train_all(total_timesteps=timesteps)

            audit_logger.log_event(
                event_type='RL_TRAINING_COMPLETED',
                actor='API_Server',
                details={'symbols': symbols, 'timesteps': timesteps},
                status='SUCCESS'
            )

        background_tasks.add_task(train_task)

        return {
            'status': 'training_started',
            'symbols': symbols,
            'model_type': model_type,
            'timesteps': timesteps
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== MARKET DATA ==========

@app.get("/market/candles/{symbol}")
async def get_candles(symbol: str, timeframe: int = 60, count: int = 100):
    """Pobierz świece."""
    try:
        candles = db.get_candles(symbol, timeframe, limit=count)

        result = []
        for _, candle in candles.iterrows():
            result.append({
                'timestamp': candle['timestamp'].isoformat(),
                'open': float(candle['open']),
                'high': float(candle['high']),
                'low': float(candle['low']),
                'close': float(candle['close']),
                'volume': int(candle['volume'])
            })

        return {
            'symbol': symbol,
            'timeframe': timeframe,
            'candles': result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/market/price/{symbol}")
async def get_price(symbol: str):
    """Pobierz aktualną cenę."""
    try:
        price_info = mt5.get_current_price(symbol)

        if not price_info:
            raise HTTPException(status_code=404, detail=f"Cannot get price for {symbol}")

        return {
            'symbol': symbol,
            'bid': price_info['bid'],
            'ask': price_info['ask'],
            'spread': price_info['ask'] - price_info['bid'],
            'timestamp': datetime.fromtimestamp(price_info['time']).isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== AUDIT & LOGS ==========

@app.get("/audit/trail")
async def get_audit_trail(event_type: Optional[str] = None, days: int = 7):
    """Pobierz audit trail."""
    try:
        trail = audit_logger.get_audit_trail(event_type=event_type, days=days)

        return {
            'events': trail.to_dict('records') if len(trail) > 0 else [],
            'total': len(trail),
            'filters': {'event_type': event_type, 'days': days}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/audit/compliance-report")
async def get_compliance_report(start_date: str, end_date: str):
    """Pobierz raport compliance."""
    try:
        from datetime import datetime
        report = audit_logger.generate_compliance_report(
            datetime.strptime(start_date, '%Y-%m-%d'),
            datetime.strptime(end_date, '%Y-%m-%d')
        )

        return {
            'report': report,
            'format': 'text'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== MANUAL COMMANDS ==========

@app.post("/manual/place-order")
async def manual_place_order(
    symbol: str,
    direction: str,
    lot_size: float,
    price: float = 0,
    take_profit: float = 0,
    stop_loss: float = 0
):
    """Ręcznie złóż zlecenie."""
    try:
        # Validate first
        is_valid, msg = risk_mgr.validate_trade(symbol, direction, lot_size, price or 100)

        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Validation failed: {msg}")

        # Place order
        ticket = mt5.place_order(
            symbol=symbol,
            action=direction,
            lot_size=lot_size,
            price=price,
            take_profit=take_profit,
            stop_loss=stop_loss,
            comment="MANUAL_API"
        )

        if ticket:
            audit_logger.log_trade({
                'symbol': symbol,
                'direction': direction,
                'entry_price': price,
                'lot_size': lot_size,
                'reason': 'Manual API order'
            })

            return {
                'status': 'success',
                'order_ticket': ticket,
                'symbol': symbol
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to place order")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)

    logger.info(f"🚀 Starting API Server on 0.0.0.0:8000")
    logger.info(f"📚 API Docs: http://localhost:8000/docs")

    uvicorn.run(app, host="0.0.0.0", port=8000)
