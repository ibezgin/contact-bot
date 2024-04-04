import re

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, CommandStart, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, callback_query

from keyboards.inline import get_callback_btns
from keyboards.reply import get_keyboard

user_private_router = Router()


# noinspection PyTypeChecker
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет, дорогой друг!👋\n\nЯ - твой надежный помощник в поиске интересных собеседников и "
        "качественного общения. Разработчики с огромной любовью создавали меня, чтобы облегчить "
        "непростой путь к настоящей дружбе и искреннему общению.\n\nЗдесь ты можешь найти новых "
        "знакомых, обменяться мыслями, делиться радостью и поддерживать друг друга. Доверься мне, "
        "и я помогу тебе раскрыться в новых взглядах и возможностях.\n\n"
        "Давай говорить, слушать и создавать настоящие связи. "
        "Спасибо, что выбрал меня, и пусть каждое общение будет для тебя особенным и ценным! 💬✨",
        reply_markup=get_keyboard(
            "Создать анкету",
            placeholder="Выберите действие",
            sizes=(1,)
        ),
    )


# noinspection PyTypeChecker
class Form(StatesGroup):
    age = State()
    gender = State()
    name = State()
    city = State()
    purpose = State()
    WaitingForYesNo = State()
    image = State()
    contact = State()

    texts = {
        'Form:age': 'Введите возраст заново:',
        'Form:gender': 'Выберите пол заново:',
        'Form:name': 'Введите имя заново:',
        'Form:city': 'Введите город заново:',
        'Form:purpose': 'Выберите цель заново:',
        'Form:WaitingForYesNo': 'Хотите добавить фото?',
        'Form:image': 'Добавьте фото',
        'Form:contact': 'Оставьте контакт заново:',
    }
    keyboards = {
        'Form:age': get_keyboard("Отмена",
                                 placeholder="Выберите 'отмена' или введите возраст",
                                 sizes=(1,)),
        'Form:gender': get_keyboard("Мужской",
                                    "Женский",
                                    "Отмена",
                                    "Предыдущий вопрос",
                                    placeholder="Выберите пол",
                                    sizes=(2, 1)),
        'Form:name': get_keyboard("Отмена",
                                  "Предыдущий вопрос",
                                  placeholder="Введи имя",
                                  sizes=(1,)),
        'Form:city': get_keyboard("Отмена",
                                  "Предыдущий вопрос",
                                  placeholder="Введи город",
                                  sizes=(1,)),
        'Form:purpose': get_keyboard("поиск отношений",
                                     "просто общение",
                                     "Отмена",
                                     "Предыдущий вопрос",
                                     placeholder="Выбери вариант ответа",
                                     sizes=(2, 1)),
        'Form:WaitingForYesNo': get_keyboard("Да",
                                             "Нет",
                                             "Отмена",
                                             "Предыдущий вопрос",
                                             placeholder="Выбери вариант ответа",
                                             sizes=(2, 1)),
        'Form:image': get_keyboard("Отмена",
                                   "Предыдущий вопрос",
                                   placeholder="Добавьте фото",
                                   sizes=(2, 1)),
        'Form:contact': get_keyboard("Отмена",
                                     "Предыдущий вопрос",
                                     placeholder="Оставь контакт для связи",
                                     sizes=(1,)),
    }


# noinspection PyTypeChecker
@user_private_router.message(StateFilter(None),
                             or_f(Command('create-form'), F.text.lower().contains("создать анкету")))
async def create_form(message: types.Message, state: FSMContext):
    await message.answer("Класс! Ты на шаг ближе к новым знакомствам! А теперь давай ответим на вопросы анкеты",
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer("1 вопрос: сколько тебе лет?",
                         reply_markup=get_keyboard(
                             "Отмена",
                             placeholder="Выберите 'отмена' или введите возраст",
                             sizes=(1,)))
    await state.set_state(Form.age)


# noinspection PyTypeChecker
@user_private_router.message(StateFilter('*'), Command("отмена"))
@user_private_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=get_keyboard(
        "Создать анкету",
        placeholder="Выберите действие",
        sizes=(1,)))


@user_private_router.message(StateFilter('*'), Command("предыдущий вопрос"))
@user_private_router.message(StateFilter('*'), F.text.casefold() == "предыдущий вопрос")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == Form.age:
        await message.answer('Предыдущего вопроса не было. Выберите "отмена" или введите возраст.')
        return

    previous = None
    for step in Form.__all_states__:
        if step.state == current_state:
            if previous is not None:
                await state.set_state(previous)
                question_text = Form.texts.get(previous.state, "Вопрос не найден.")
                keyboard = Form.keyboards.get(previous.state)
                await message.answer(f"Ок, вы вернулись к предыдущему вопросу \n {Form.texts[previous.state]}",
                                     reply_markup=keyboard)
                return
        previous = step


# noinspection PyTypeChecker
@user_private_router.message(Form.age, F.text)
async def add_age(message: types.Message, state: FSMContext):
    age = int(message.text)
    if age < 16:
        await message.answer("Извини, только людям больше 16 лет.")
        return

    await state.update_data(age=message.text)
    await message.answer("2 вопрос: какого ты пола?", reply_markup=get_keyboard(
        "Мужской",
        "Женский",
        "Отмена",
        "Предыдущий вопрос",
        placeholder="Выберите пол",
        sizes=(2, 1)))
    await state.set_state(Form.gender)


@user_private_router.message(Form.age)  # если кто-то решит фото или другую хрень отправить на вопрос о возрасте
async def add_age2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели неправильные данные, введите возраст.")


# noinspection PyTypeChecker
@user_private_router.message(Form.gender, F.text)
async def add_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("3 вопрос: как тебя зовут?", reply_markup=get_keyboard(
        "Отмена",
        "Предыдущий вопрос",
        placeholder="Введи имя",
        sizes=(1,)))
    await state.set_state(Form.name)


@user_private_router.message(Form.gender)  # если кто-то решит фото или другую хрень отправить на вопрос о поле
async def add_gender2(message: types.Message, state: FSMContext):
    await message.answer("Вводить ничего не нужно, просто выберите пол")


# noinspection PyTypeChecker
@user_private_router.message(Form.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("4 вопрос: из какого ты города?", reply_markup=get_keyboard(
        "Отмена",
        "Предыдущий вопрос",
        placeholder="Введи город",
        sizes=(1,)))
    await state.set_state(Form.city)


@user_private_router.message(Form.name)  # если кто-то решит фото отправить на вопрос об имени
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer("Просто введи имя")


# noinspection PyTypeChecker
@user_private_router.message(Form.city, F.text)
async def add_city(message: types.Message, state: FSMContext):
    x = re.compile(r'[а-яА-Яa-zA-Z]+')
    z = message.text
    if not x.match(z):
        await message.answer("Используй только буквы")
    else:
        await state.update_data(city=message.text)
        await message.answer("5 вопрос: зачем тебе эта анкета?", reply_markup=get_keyboard(
            "поиск отношений",
            "просто общение",
            "Отмена",
            "Предыдущий вопрос",
            placeholder="Выбери вариант ответа",
            sizes=(2, 1)))
        await state.set_state(Form.purpose)


# noinspection PyTypeChecker
@user_private_router.message(Form.purpose, F.text)
async def question(message: types.Message, state: FSMContext):
    await state.update_data(purpose=message.text)
    await message.answer("Добавим фото?", reply_markup=get_keyboard(
        "Да",
        "Нет",
        "Отмена",
        "Предыдущий вопрос",
        placeholder="Выбери вариант ответа",
        sizes=(2, 1)))
    await state.set_state(Form.WaitingForYesNo)


# noinspection PyTypeChecker
@user_private_router.message(Form.WaitingForYesNo, F.text)
async def process_yes_no(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await message.answer("Добавьте фото(до 3)", reply_markup=get_keyboard(
            "Отмена",
            placeholder="Добавь фото",
            sizes=(1,)))
        await state.set_state(Form.image)
    elif message.text.lower() == "нет":
        await state.update_data(image=message.text)
        await message.answer("ОК, тогда пропустим этот шаг.")
        await message.answer("Можете оставить свои контакты для связи?", reply_markup=get_keyboard(
            "Отмена",
            "Предыдущий вопрос",
            placeholder="Оставь контакт для связи",
            sizes=(1,)))
        await state.set_state(Form.contact)
    else:
        await message.answer("Пожалуйста, выберите Да или Нет")


# noinspection PyTypeChecker
@user_private_router.message(Form.image, F.photo)
async def add_image(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    uploaded_images = user_data.get("uploaded_images", [])

    if len(uploaded_images) < 3:
        uploaded_images.append(message.photo[-1].file_id)
        await state.update_data(uploaded_images=uploaded_images)
        await message.answer(
            f"Фото {len(uploaded_images)} загружено. Можете загрузить ещё или отправьте skip для продолжения.")

        if len(uploaded_images) == 3:
            await message.answer("Можете оставить свои контакты для связи?", reply_markup=get_keyboard(
                "Отмена",
                "Предыдущий вопрос",
                placeholder="Оставь контакт для связи",
                sizes=(1,)))
            await state.set_state(Form.contact)
    else:
        await message.answer("Уже загружено максимальное количество фото.")


# noinspection PyTypeChecker
@user_private_router.message(or_f(Command("skip"), F.text.lower().contains("skip")), Form.image)
async def skip_image_upload(message: types.Message, state: FSMContext):
    await message.answer("Добавление фото пропущено.")
    await message.answer("Можете оставить свои контакты для связи?", reply_markup=get_keyboard(
        "Отмена",
        "Предыдущий вопрос",
        placeholder="Оставь контакт для связи",
        sizes=(1,)))
    await state.set_state(Form.contact)


@user_private_router.message(Form.purpose)
async def add_purpose2(message: types.Message, state: FSMContext):
    await message.answer("Просто выбери вариант")


# noinspection PyTypeChecker
@user_private_router.message(Form.contact, F.text)
async def add_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer("Готово! Начнём искать собеседника?", reply_markup=get_keyboard(
        "Поиск собеседника",
        "Редактировать анкету",
        "Предыдущий вопрос",
        placeholder="Выберите действие",
        sizes=(2, 1)))
    data = await state.get_data()
    images_info = data.get('image', '')
    if 'uploaded_images' in data and data['uploaded_images']:
        images_info = ', '.join(data['uploaded_images'])
    profile_info = (
        "Ваша анкета:\n"
        f"Имя: {data['name']}\n"
        f"Пол: {data['gender']}\n"
        f"Возраст: {data['age']}\n"
        f"Город: {data['city']}\n"
        f"Цель: {data['purpose']}\n"
        f"Контакт: {data['contact']}\n"
        f"Фото: {images_info}\n"
    )
    await message.answer(profile_info)
    await state.clear()


@user_private_router.message(Form.purpose)
async def add_contact2(message: types.Message, state: FSMContext):
    await message.answer("оставь ссылку")