"""
Утилиты для интеграции с GigaChat: получение LLM и генерация советов.
"""
import asyncio
from functools import cache
from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import HumanMessage
from app.config import get_settings
import logging

def get_gigachat_llm():
    settings = get_settings()
    token = settings.gigachat_token
    verify_ssl = settings.verify_ssl_certs
    logging.info(f"GigaChat: токен {'найден' if token else 'НЕ найден'}: {repr(token)[:8]}..., verify_ssl_certs={verify_ssl}")
    if not token:
        return None
    return GigaChat(
        credentials=token,
        model="GigaChat",
        verify_ssl_certs=verify_ssl,
        streaming=False,
        temperature=1.0)

async def get_gigachat_tip():
    llm = get_gigachat_llm()
    if not llm:
        logging.info("GigaChat: llm не инициализирован, совет будет из списка.")
        return None
    try:
        resp = await asyncio.to_thread(
            llm.invoke,
            [HumanMessage(content="Дай рандомный, короткий финансовый совет для пользователя Telegram-бота.")],
        )
        logging.info("GigaChat: совет успешно получен от LLM.")
        return resp.content.strip()
    except Exception as e:
        logging.error(f"GigaChat: ошибка при получении совета: {e}")
        return None 