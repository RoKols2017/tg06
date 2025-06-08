from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardRemove)

"""
Клавиатуры для основного меню Telegram-бота.
"""

def main_menu() -> ReplyKeyboardMarkup:
    """Главное меню бота (Reply-клавиатура)."""
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text="💳 Регистрация")],
            [KeyboardButton(text="💱 Курс валют"), KeyboardButton(text="💡 Совет")],
            [KeyboardButton(text="📊 Личные финансы")],
        ],
    )

def hide() -> ReplyKeyboardRemove:
    """Убирает клавиатуру."""
    return ReplyKeyboardRemove()
