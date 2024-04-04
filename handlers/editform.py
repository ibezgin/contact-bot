@user_private_router.message(or_f(Command('edit-form'), F.text.lower().contains("редактировать анкету")))
async def edit_form(message: types.Message):
    await message.answer("Что хотите отредактировать?", reply_markup=get_callback_btns(btns={
        "Возраст": 'edit_age',
        "Пол": 'edit_gender',
        "Имя": 'edit_name',
        "Город": 'edit_city',
        "Цель": 'edit_purpose',
        "Контакты": 'edit_contact'
    })
                         )


@user_private_router.callback_query(lambda call: call.data.startswith('edit_'))
async def process_edit_field(call: types.CallbackQuery, state: FSMContext):
    field = call.data[len("edit_"):]
    state_class = getattr(Form, field, None)
    if state_class:
        await state.set_state(state_class)
        await call.bot.send_message(chat_id=call.from_user.id, text=f"Введите новое значение для {field}.")
    else:
        await call.bot.send_message(chat_id=call.from_user.id, text="Выбранное поле для редактирования не найдено.")
    await call.answer()


@user_private_router.message(Form.age)
async def edit_age(message: types.Message, state: FSMContext):
    new_age = message.text
    await state.update_data(age=new_age)
    await message.answer("Возраст успешно обновлен.")
    await send_profile(message, state)
    await state.clear()


@user_private_router.message(Form.gender)
async def edit_gender(message: types.Message, state: FSMContext):
    new_gender = message.text
    await state.update_data(gender=new_gender)
    await message.answer("Пол успешно обновлен")
    await send_profile(message, state)
    await state.clear()


@user_private_router.message(Form.name)
async def edit_name(message: types.Message, state: FSMContext):
    new_name = message.text
    await state.update_data(name=new_name)
    await message.answer("Имя успешно обновлено")
    await send_profile(message, state)
    await state.clear()


@user_private_router.message(Form.city)
async def edit_city(message: types.Message, state: FSMContext):
    new_city = message.text
    await state.update_data(city=new_city)
    await message.answer("Город успешно обновлен")
    await send_profile(message, state)
    await state.clear()


@user_private_router.message(Form.purpose)
async def edit_purpose(message: types.Message, state: FSMContext):
    new_purpose = message.text
    await state.update_data(purpose=new_purpose)
    await message.answer("Цель успешно обновлена")
    await send_profile(message, state)
    await state.clear()


@user_private_router.message(Form.contact)
async def edit_contact(message: types.Message, state: FSMContext):
    new_contact = message.text
    await state.update_data(contact=new_contact)
    await message.answer("Контакты успешно обновлены")
    await send_profile(message, state)
    await state.clear()


async def send_profile(message: types.Message, state: FSMContext):
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
