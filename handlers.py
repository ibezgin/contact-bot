from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import keyboards as kb
import ReadeR as RR

router = Router()


class Process(StatesGroup):
    age_1 = State()
    searching = State()

class Find(StatesGroup):
    age_2 = State()
    city = State()
count = 0


@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer("Привет! Введите /find, чтобы начать поиск. Команда /help для списка команд.")

@router.message(Command("stop"))
async def stop(message: Message):
    await message.answer("Настройки фильтров очищены")
    await state.clear()

@router.message(Command("help"))
async def help(message: Message):
    await message.answer("Список команд: \n/start - Запускает бота"
                         "\n/help - Вызывает окно помощи"
                         "\n/find - Запускает функцию поиска"
                         "\n/stop - Сбрасывает фильтры")

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
        await state.update_data(gender="Всё равно")
        data = await state.get_data()
        await message.answer(f'Настройка фильтров завершена.'
                             f'\nВаши фильтры:\nГород: {data["city"]}\nВозраст: {data["age_2"]}'
                             f'\nДля сброса нажмите кнопку стоп',
                             reply_markup=kb.further)
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
    data = await state.get_data()
    await message.answer(f'Настройка фильтров завершена.'
                         f'\nВаши фильтры:\nГород: {data["city"]}\nВозраст: {data["age_2"]}'
                         f'\nДля сброса нажмите кнопку стоп',
                        reply_markup=kb.further)
    await state.set_state(Process.searching)

@router.message(Process.searching)
async def find_searching(message: Message, state: FSMContext):
    data = await state.get_data()
    global count
    if data["age_2"] == "от 18 до 25":
        min_age = 18
        max_age = 25
    elif data["age_2"] == "от 25 до 35":
        min_age = 25
        max_age = 35
    elif data["age_2"] == "от 35 до 45":
        min_age = 35
        max_age = 45
    elif data["age_2"] == "Всё равно":
        min_age = 18
        max_age = 1000
    if data["city"] == "Всё равно":
        if message.text == "Продолжить":
            try:
                filtered_data = RR.filter_data_without_city(min_age, max_age)
                await message.answer(f'Имя: {filtered_data[count][0]}'
                                     f'\nГород: {filtered_data[count][1]}'
                                     f'\nВозраст: {filtered_data[count][2]}'
                                     f'\nПол: {filtered_data[count][3]}',
                                     reply_markup=kb.like_or_dislike)
                count += 1
            except IndexError:
                await message.answer("Пользователи по заданым фильтрам закончились")
        elif message.text == "Лайк":
            await message.answer("Здесь могла быть ваша функция создания чата")
        elif message.text == "Дизлайк":
            try:
                filtered_data = RR.filter_data_without_city(min_age, max_age)
                await message.answer(f'Имя: {filtered_data[count][0]}'
                                     f'\nГород: {filtered_data[count][1]}'
                                     f'\nВозраст: {filtered_data[count][2]}'
                                     f'\nПол: {filtered_data[count][3]}',
                                     reply_markup=kb.like_or_dislike)
                count += 1
            except IndexError:
                await message.answer("Пользователи по заданым фильтрам закончились")
    else:
        if message.text == "Продолжить":
            try:
                filtered_data = RR.filter_data(data["city"], min_age, max_age)
                await message.answer(f'Имя: {filtered_data[count][0]}'
                                     f'\nГород: {filtered_data[count][1]}'
                                     f'\nВозраст: {filtered_data[count][2]}'
                                     f'\nПол: {filtered_data[count][3]}',
                                     reply_markup=kb.like_or_dislike)
                count += 1
            except IndexError:
                await message.answer("Пользователи по заданым фильтрам закончились")
        elif message.text == "Лайк":
            await message.answer("Здесь могла быть ваша функция создания чата")
        elif message.text == "Дизлайк":
            try:
                filtered_data = RR.filter_data(data["city"], min_age, max_age)
                await message.answer(f'Имя: {filtered_data[count][0]}'
                                     f'\nГород: {filtered_data[count][1]}'
                                     f'\nВозраст: {filtered_data[count][2]}'
                                     f'\nПол: {filtered_data[count][3]}',
                                     reply_markup=kb.like_or_dislike)
                count += 1
            except IndexError:
                await message.answer("Пользователи по заданым фильтрам закончились")