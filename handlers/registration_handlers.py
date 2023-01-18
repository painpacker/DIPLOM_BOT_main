from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import message

from servises.registration_servises import user_service
from states.registration_state import RegistrationState


async def start_registration(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationState.name.state)
    await callback.message.answer('Введите Имя')


async def load_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
        data['user_id'] = msg.from_user.id

    await RegistrationState.next()
    await msg.answer('Введите ваш номер телефона(7 последних цифр)')


async def load_phone(msg: types.Message, state=FSMContext):
    if len(msg.text) == 7:
        async with state.proxy() as data:
            data['phone'] = msg.text

        await RegistrationState.next()
        await msg.answer("Введите почту")
    else:
        await msg.answer("Попробуйте ещё раз")


async def load_email(msg: types.Message, state=FSMContext):
    if '@' in msg.text:
        async with state.proxy() as data:
            data['email'] = msg.text

    print(dict(data.items()))
    user_service.add_user(dict(data.items()))

    await state.finish()
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("I want to continue!", callback_data="go_next"))
    inline_kb.add(types.InlineKeyboardButton("I want to talk with Admin!", callback_data="admin"))
    await msg.answer("""
    If you want to get to the main menu, press the first button.
    
    If you wish to write to the administrator, press the second.
    """, reply_markup= inline_kb)



def setup(dp: Dispatcher):
    dp.register_callback_query_handler(start_registration, text='registration_1')
    dp.register_message_handler(load_name, state=RegistrationState.name)
    dp.register_message_handler(load_email, state=RegistrationState.email)
    dp.register_message_handler(load_phone, state=RegistrationState.phone)


