"""
ORM-модели: пользователь и его категории расходов.
"""

from sqlalchemy import String, ForeignKey, Numeric, func, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from decimal import Decimal

class Base(DeclarativeBase):
    """Базовый класс для моделей."""

class User(Base):
    """
    Модель пользователя Telegram-бота.
    Поля:
        id: Внутренний идентификатор (PK).
        tg_id: Telegram ID пользователя (уникальный).
        full_name: Имя пользователя.
        categories: Категории расходов пользователя (связь).
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(256))

    categories: Mapped[list["Category"]] = relationship(back_populates="owner")

class Category(Base):
    """
    Модель категории расходов пользователя.
    Поля:
        id: Внутренний идентификатор (PK).
        name: Название категории.
        spent: Сумма расходов по категории.
        owner_id: Внешний ключ на пользователя.
        owner: Связь с пользователем.
    """
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    spent: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped[User] = relationship(back_populates="categories")
