from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from keyboard import make_row_keyboard

career_choice_router = Router()

available_prof_names = ["Разработчик", "Аналитик", "Тестировщик"]
available_prof_grade = ["Junior", "Middle", "Senior"]


class ChoiceProfNames(StatesGroup):
    choosing_prof_names = State()
    choosing_prof_grade = State()


@career_choice_router.message(Command('prof'))
@career_choice_router.message(F.text == "Профессии")
async def cmd_prof(message: types.Message, state: FSMContext):
    await message.answer(text="Выбери профессию",
                         reply_markup=make_row_keyboard(available_prof_names))
    await state.set_state(ChoiceProfNames.choosing_prof_names)


# Проверка, если пользователь правильно выбрал профессию предлагаем выбрать уровень
@career_choice_router.message(ChoiceProfNames.choosing_prof_names,
                              F.text.in_(available_prof_names))
async def prof_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_prof=message.text.lower())
    await message.answer(text="Выбери свой уровень:",
                         reply_markup=make_row_keyboard(available_prof_grade))
    await state.set_state(ChoiceProfNames.choosing_prof_grade)


# Проверка, если пользователь ввел свою профессию (а не из списка) предлагаем повторить выбор
@career_choice_router.message(ChoiceProfNames.choosing_prof_names)
async def prof_chosen_incorrectly(message: types.Message):
    await message.reply(text="Выбери профессию из списка!!!",
                        reply_markup=make_row_keyboard(available_prof_names))


# Проверка, если пользователь правильно выбрал уровень выводим выбранные профессию и уровень
@career_choice_router.message(ChoiceProfNames.choosing_prof_grade,
                              F.text.in_(available_prof_grade))
async def grad_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали {message.text.lower()} уровень {
        user_data.get('chosen_prof')}",
        reply_markup=ReplyKeyboardRemove())
    await state.clear()


# Проверка, если пользователь ввел свой уровень (а не из списка) предлагаем повторить выбор
@career_choice_router.message(ChoiceProfNames.choosing_prof_grade)
async def grade_chosen_incorrectly(message: types.Message):
    await message.reply(text="Выбери уровень из списка!!!",
                        reply_markup=make_row_keyboard(available_prof_grade))
