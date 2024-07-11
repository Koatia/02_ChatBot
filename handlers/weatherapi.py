from datetime import datetime
from dotenv import load_dotenv
import requests
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение токена из переменных окружения
weather_api = os.getenv("weather_api")
if not weather_api:
    raise ValueError("No weather_api provided")


def format_date(date_str):
    month_names = {
        "01": "января",
        "02": "февраля",
        "03": "марта",
        "04": "апреля",
        "05": "мая",
        "06": "июня",
        "07": "июля",
        "08": "августа",
        "09": "сентября",
        "10": "октября",
        "11": "ноября",
        "12": "декабря",
    }
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime(f"%d {month_names[date_obj.strftime('%m')]} %Y г.")


def get_emoji(condition):
    if "snow" in condition.lower():
        return "❄️"
    elif "cloudy" in condition.lower():
        return "☁️"
    elif "rain" in condition.lower():
        return "🌧️"
    elif "fog" in condition.lower():
        return "🌫️"
    elif "sunny" in condition.lower():
        return "🌞"
    elif "blizzard" in condition.lower():
        return "💨"
    elif "overcast" in condition.lower():
        return "⛅"
    elif "lightning" in condition.lower():
        return "🌩️"
    # добавьте другие условия и соответствующие эмодзи по желанию
    else:
        return ""


async def get_weather(city):
    api_key = weather_api
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=10"

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        now = f"<b>Сейчас в {city}</b> {weather_data['current']['condition']['text']} <b>{weather_data['current']['temp_c']}°C</b>\n"
        forecast_message = f"{now}<b>Прогноз погоды на 10 дней:</b>\n\n"

        for day in weather_data["forecast"]["forecastday"]:
            date = format_date(day["date"])
            condition = day["day"]["condition"]["text"]
            max_temp = day["day"]["maxtemp_c"]
            min_temp = day["day"]["mintemp_c"]
            wind_speed = day["day"]["maxwind_kph"]

            emoji = get_emoji(condition)

            forecast_message += f"<b>{date}:</b>\n{emoji} <i>{condition}</i>, температура от <i>{min_temp}°C</i> до <i>{max_temp}°C</i>, ветер до <i>{wind_speed} км/ч</i>\n"

        return forecast_message

    except requests.RequestException as e:
        print(f"Ошибка запроса к API: {e}")
        return "Не удалось получить данные о погоде."
