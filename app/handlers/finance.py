from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from decimal import Decimal, InvalidOperation
from sqlalchemy import select

from app.db.models import Category, User
from app.db.session import new_session
from app.utils.messages import (
    ASK_CATEGORY, ASK_AMOUNT, INVALID_AMOUNT, REGISTER_FIRST, EXPENSE_SAVED
)

router = Router(name="finance")

class ExpenseWizard(StatesGroup):
    """Сценарий для пошагового ввода категории и суммы расхода пользователя (FSM)."""
    waiting_for_category = State()
    waiting_for_amount = State()

@router.message(F.text.lower() == "📊 личные финансы")
async def ask_category(message: Message, state: FSMContext) -> None:
    await state.set_state(ExpenseWizard.waiting_for_category)
    await message.reply(ASK_CATEGORY)

@router.message(ExpenseWizard.waiting_for_category)
async def save_category(message: Message, state: FSMContext) -> None:
    await state.update_data(category=message.text.strip()[:60])
    await state.set_state(ExpenseWizard.waiting_for_amount)
    await message.reply(ASK_AMOUNT)

@router.message(ExpenseWizard.waiting_for_amount)
async def save_amount(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        amount = Decimal(message.text.replace(",", "."))
    except InvalidOperation:
        await message.reply(INVALID_AMOUNT)
        return

    async with new_session() as session:
        user: User | None = await session.scalar(
            select(User).where(User.tg_id == message.from_user.id)
        )
        if not user:
            await message.reply(REGISTER_FIRST)
            await state.clear()
            return

        session.add(Category(name=data["category"], spent=amount, owner=user))

    await message.reply(EXPENSE_SAVED, reply_markup=None)
    await state.clear()
