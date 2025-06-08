"""
Запрос курса USD/RUB и EUR/RUB через ExchangeRate-API (асинхронно).
Метод кешируется на 10 минут, чтобы не бомбить API.
"""

from datetime import datetime, timedelta
from typing import TypedDict

import aiohttp
from functools import wraps
from app.config import get_settings

class Rate(TypedDict):
    usd: float
    eur: float

_cache: Rate | None = None
_expires_at: datetime | None = None

def _cached(ttl: timedelta):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            global _cache, _expires_at
            if _cache and _expires_at and _expires_at > datetime.utcnow():
                return _cache
            _cache = await fn(*args, **kwargs)
            _expires_at = datetime.utcnow() + ttl
            return _cache
        return wrapper
    return decorator

@_cached(ttl=timedelta(minutes=10))
async def get_rates() -> Rate:
    """Возвращает кортеж (USD→RUB, EUR→RUB)."""
    settings = get_settings()
    url = f"https://v6.exchangerate-api.com/v6/{settings.exchange_api_key.get_secret_value()}/latest/USD"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as resp:
            resp.raise_for_status()
            data = await resp.json()

    usd_to_rub = data["conversion_rates"]["RUB"]
    eur_to_usd = data["conversion_rates"]["EUR"]
    return {"usd": usd_to_rub, "eur": eur_to_usd * usd_to_rub}
