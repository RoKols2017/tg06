"""
Обработчики регистрации и аутентификации пользователей Telegram-бота.
"""
from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select

from app.db.session import new_session
from app.db.models import User
from app.utils.messages import ALREADY_REGISTERED, REGISTER_SUCCESS

router = Router(name="auth")

@router.message(F.text.lower() == "💳 регистрация")
async def register_user(message: Message) -> None:
    """Регистрируем пользователя в БД."""
    tg_id = message.from_user.id
    full_name = message.from_user.full_name

    async with new_session() as session:
        result = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        user = result.scalar_one_or_none()
        if user:
            await message.reply(ALREADY_REGISTERED)
            return
        session.add(User(tg_id=tg_id, full_name=full_name))
    await message.reply(REGISTER_SUCCESS)
