from aiogram import Router, F
from aiogram.types import Message
from app.utils.exchange import get_rates
from app.utils.messages import RATES_TEMPLATE

router = Router(name="rates")

@router.message(F.text.lower() == "💱 курс валют")
async def show_rates(message: Message) -> None:
    """Показываем актуальные курсы USD и EUR к рублю."""
    rates = await get_rates()
    await message.reply(RATES_TEMPLATE.format(usd=rates['usd'], eur=rates['eur']))
