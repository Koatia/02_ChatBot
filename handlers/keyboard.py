import math

from aiogram import types


# button1 = types.KeyboardButton(text="Показать лису")
# button2 = types.KeyboardButton(text="Информация")
# button3 = types.KeyboardButton(text="/dice")

# kb1 = [
#   [button1, button2, button3],
# ]

# keyword1 = types.ReplyKeyboardMarkup(
#   keyboard=kb1,
#   resize_keyboard=True,
# )

# Функция создает клавиатуру из списка наименований кнопок
# buttons_list = ["О боте", "Показать лису", "Профессии"]
# def make_row_keyboard(items: list[str]) -> types.ReplyKeyboardMarkup:
#   row = [types.KeyboardButton(text=item) for item in items]
#   return types.ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


# buttons_list = [("О боте", "info"), ("Показать лису", "fox"),
#                 ("Профессии", "prof")]
def make_inline_keyboard(buttons_list) -> types.InlineKeyboardMarkup:
    if not buttons_list:
        raise ValueError("Список кнопок пуст")

    print("Создание клавиатуры с кнопками:", buttons_list)  # Для отладки
    row_width = math.ceil(math.sqrt(len(buttons_list)))

    # Создаем список кнопок
    buttons = [
        types.InlineKeyboardButton(text=button_text, callback_data=command)
        for button_text, command in buttons_list
    ]

    # Передаем список кнопок напрямую в InlineKeyboardMarkup
    keyboard = types.InlineKeyboardMarkup(row_width=row_width,
                                          inline_keyboard=[buttons])
    return keyboard
