from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import keyboards as kb

router = Router()


class Process(StatesGroup):
    age_1 = State()
    searching = State()

class Find(StatesGroup):
    age_2 = State()
    city = State()


@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer("Привет! Введите /find, чтобы начать поиск.")

@router.message(Command("stop"))
async def stop(message: Message):
    await message.answer("Настройки фильтров очищены")
    await state.clear()

@router.message(Command("find"))
async def find_start(message: Message, state: FSMContext):
    await message.answer("Будем настраивать фильтры?",
                         reply_markup=kb.filters)
    await state.set_state(Process.age_1)

@router.message(Process.age_1)
async def find_age_1(message: Message, state: FSMContext):
    if message.text == "Да":
        await message.answer("Выберите предпочтительный возраст",
                             reply_markup=kb.age)
        await state.set_state(Find.age_2)
    elif message.text == "Нет":
        await state.update_data(age_2="Всё равно")
        await state.update_data(city="Всё равно")
        await message.answer('Настройка фильтров завершена. Начинаем поиск?',
                             reply_markup=kb.filters)
        await state.set_state(Process.searching)

@router.message(Find.age_2)
async def find_age_2(message: Message, state: FSMContext):
    await state.update_data(age_2=message.text)
    await message.answer("Введите название города",
                         reply_markup=kb.city)
    await state.set_state(Find.city)

@router.message(Find.city)
async def find_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer('Настройка фильтров завершена. Начинаем поиск?',
                        reply_markup=kb.filters)
    await state.set_state(Process.searching)

@router.message(Process.searching)
async def find_searching(message: Message, state: FSMContext):
    if message.text == "Да":
        data = await state.get_data()
        await message.answer(f'Ваши фильтры:\nГород: {data["city"]}\nВозраст: {data["age_2"]}')
    elif message.text == "Нет":
        await message.answer("Настройки фильтров очищены")
        await state.clear()