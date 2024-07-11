import requests
from dotenv import load_dotenv
import os


def get_bot_info(token):
    api_url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if data["ok"]:
            return data["result"]
        else:
            print(f"Ошибка: {data['description']}")
    else:
        print(f"Ошибка HTTP: {response.status_code}")


if __name__ == "__main__":
    # Загрузка переменных окружения из .env файла
    load_dotenv()
    # Получение токена из переменных окружения
    token_api = os.getenv("TOKEN_API")
    token = token_api  # Замените на свой токен
    bot_info = get_bot_info(token)

    if bot_info:
        print("Информация о боте:")
        print(f"Имя бота:\t{bot_info['username']}")
        print(f"ID бота:\t{bot_info['id']}")
        print(f"Язык бота:\t{bot_info.get('language_code', 'не указан')}")
