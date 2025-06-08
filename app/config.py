"""
Настройки приложения (Pydantic-settings ≥ 2.9).

✓ алиасы переменных окружения
✓ .env в корне проекта
✓ SecretStr для токена
"""

from __future__ import annotations

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


class Settings(BaseSettings):
    """
    Конфигурация приложения через pydantic-settings.
    Параметры:
        bot_token: Токен Telegram-бота (секрет).
        database_url: URL для подключения к базе данных.
        gigachat_token: Токен для доступа к GigaChat (опционально).
        verify_ssl_certs: Проверять SSL-сертификаты при подключении к GigaChat (bool).
    """
    # 1. BOT_TOKEN → bot_token
    bot_token: SecretStr = Field(..., alias="BOT_TOKEN")

    # 2. DATABASE_URL → database_url
    database_url: str = Field(
        "sqlite+aiosqlite:///./finance.db",
        alias="DATABASE_URL",
    )

    # 3. GIGACHAT_TOKEN → gigachat_token
    gigachat_token: str | None = Field(None, alias="GIGACHAT_TOKEN")

    # 4. VERIFY_SSL_CERTS → verify_ssl_certs
    verify_ssl_certs: bool = Field(True, alias="VERIFY_SSL_CERTS")

    # 5. EXCHANGE_API_KEY → exchange_api_key
    exchange_api_key: SecretStr = Field(..., alias="EXCHANGE_API_KEY")

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",           # игнорировать лишние переменные
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Singleton-доступ: импортируйте `get_settings()` где угодно."""
    return Settings()


if __name__ == "__main__":  # pragma: no cover
    print("GigaChat token:", repr(get_settings().gigachat_token))