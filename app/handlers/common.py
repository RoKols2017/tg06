"""
Общие обработчики: старт, помощь, советы.
"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from app.keyboards.main import main_menu
from app.utils.messages import GREETING, get_random_tip
from app.utils.gigachat import get_gigachat_tip

router = Router(name="common")

@router.message(Command(commands=["start", "help"]))
async def start(message: Message) -> None:
    """Приветствие и вывод меню."""
    await message.answer(
        GREETING,
        reply_markup=main_menu(),
    )

@router.message(F.text.lower() == "💡 совет")
async def send_tip(message: Message) -> None:
    """Отправляет совет: сначала пытается получить от GigaChat, иначе — из локального списка."""
    tip = await get_gigachat_tip()
    if not tip:
        tip = get_random_tip()
    await message.reply(tip)
