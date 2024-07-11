from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove

from handlers import keyboard, random_fox, bot_info, weatherapi

common_router = Router()

main_menu_names = [("О боте", "info"), ("Показать лису", "fox"), ("Погода", "weather")]

# Инлайн-клавиатура для выбора города
city_menu_names = [
    ("Кстово", "weather_Kstovo"),
    ("Нижний Новгород", "weather_Nizhniy Novgorod"),
    ("Питер", "weather_St. Petersburg"),
    ("Москва", "weather_Moscow"),
]


# Хэндлер на команду /start
@common_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"<b>😊 Привет, {message.from_user.first_name}!!!</b>",
        reply_markup=keyboard.make_inline_keyboard(main_menu_names),
    )


# Хэндлер на команду /info
@common_router.callback_query(lambda c: c.data == "info")
async def info_callback(query: types.CallbackQuery):
    await query.message.answer("Информация о боте:")
    Bot_info = bot_info.get_bot_info(config.token_api)
    message_text = (
        "<b>Имя бота:</b>   <i>{}</i>\n"
        "<b>ID бота:</b>        <i>{}</i>\n"
        "<b>Язык бота:</b>  <i>{}</i>".format(
            Bot_info["username"],
            Bot_info["id"],
            Bot_info.get("language_code", "не указан"),
        )
    )

    await query.message.answer(
        message_text, reply_markup=keyboard.make_inline_keyboard(main_menu_names)
    )
    await query.answer()


# Хэндлер на команду /fox
@common_router.callback_query(lambda c: c.data == "fox")
async def info_fox(query: types.CallbackQuery):
    await query.message.answer("Держи лису 😊")
    img_fox = random_fox.fox()
    await query.message.answer_photo(img_fox)
    await query.answer()


# Хэндлер на команду /weather
@common_router.callback_query(lambda c: c.data == "weather")
async def weather_query(query: types.CallbackQuery):
    await query.message.answer(
        "Выберите название города:",
        reply_markup=keyboard.make_inline_keyboard(city_menu_names),
    )
    await query.answer()


@common_router.callback_query(lambda c: c.data.startswith("weather_"))
async def city_weather(query: types.CallbackQuery):
    # Извлечение города из callback_data
    _, city = query.data.split("_")
    # Получение и отправка погоды для выбраного города
    print(city)
    weather_data = await weatherapi.get_weather(city)
    await query.message.answer(weather_data)
    await query.answer()


# Хэндлер на сообщения
@common_router.message(F.text)
async def msg_echo(message: types.Message):
    print(message.from_user)
    name = message.from_user.first_name
    if "привет" in message.text.lower():
        await message.answer(
            f"<b>😊 Привет, {name}!!!</b>",
            reply_markup=keyboard.make_row_keyboard(main_menu_names),
        )
    elif "пока" in message.text.lower():
        await message.answer(f"Пока, {name}!!!", reply_markup=ReplyKeyboardRemove())
