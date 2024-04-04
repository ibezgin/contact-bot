from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

filters = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
],
resize_keyboard=True,
input_field_placeholder="Выберите вариант",
one_time_keyboard=True)

age = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="от 18 до 25"), KeyboardButton(text="от 25 до 35")],
    [KeyboardButton(text="от 35 до 45"), KeyboardButton(text="Всё равно")]
],
resize_keyboard=True,
input_field_placeholder="Выберите возраст",
one_time_keyboard=True)

city = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Всё равно")]
],
    resize_keyboard=True,
    input_field_placeholder="Введите город или выберите вариант 'Всё равно'",
    one_time_keyboard=True)