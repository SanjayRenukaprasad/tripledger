import redis
import httpx
from app.core.config import settings

r = redis.from_url(settings.REDIS_URL)

async def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    if from_currency == to_currency:
        return 1.0

    key = f"rate:{from_currency}:{to_currency}"

    cached = r.get(key)
    if cached:
        return float(cached)

    async with httpx.AsyncClient() as client:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = await client.get(url)
        data = response.json()

    rate = data["rates"].get(to_currency)
    if not rate:
        raise ValueError(f"Could not get rate for {from_currency} to {to_currency}")

    r.setex(key, 3600, rate)
    return float(rate)

async def convert_amount(amount: float, from_currency: str, to_currency: str) -> float:
    rate = await get_exchange_rate(from_currency, to_currency)
    return round(amount * rate, 2)