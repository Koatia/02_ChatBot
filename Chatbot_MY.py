# t.me/Kostia_Ia_bot

# Активация Виртуального Окружения `venv\Scripts\activate`
# Для сохранения списка установленных пакетов используйте команду `pip freeze > requirements.txt`
# Для установки пакетов из файла requirements.txt используйте команду `pip -r requirements.txt`

import asyncio
import logging
import os
from dotenv import load_dotenv
from handlers import common

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

# Загрузка переменных окружения из .env файла
load_dotenv()


async def main():
    logging.basicConfig(level=logging.INFO)

    # Получение токена из переменных окружения
    token_api = os.getenv("TOKEN_API")
    if not token_api:
        raise ValueError("No TOKEN_API provided")

    # Объект бот с использованием DefaultBotProperties для установки parse_mode
    bot = Bot(token=token_api, default=DefaultBotProperties(parse_mode="html"))

    # Инициализация диспетчера
    dp = Dispatcher()

    # Включение роутеров
    dp.include_router(common.common_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
