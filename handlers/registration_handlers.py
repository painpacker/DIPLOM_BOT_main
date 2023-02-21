from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from servises import registration_services
from servises.subscription_services import subscription_service

API_TOKEN = '5807659431:AAGOHNaS-xQQFVjzCbKeDRLe2lcfgTHy8kw'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
from servises.registration_services import user_service
from states.registration_state import RegistrationState



@dp.message_handler(commands=["start"])
async def welcome_commands(msg: types.Message):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Login", callback_data="login"))
    await msg.answer(f"You're Welcome! \n You need to login first", reply_markup=inline_kb)


async def load_account(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationState.name.state)
    async with state.proxy() as data:
        data['subscription'] = 0
        data['username'] = callback.from_user.username
        data['account_id'] = callback.from_user.id
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("I want to continue!", callback_data="go_next"))
    inline_kb.add(types.InlineKeyboardButton("Description", callback_data="description"))


    print(dict(data.items()))
    user_service.add_user(dict(data.items()))
    await state.finish()
    await callback.message.edit_text("""
    If you want to get to the main menu, press the first button.\n If you wish to see description, press the second.""", reply_markup=inline_kb )

def setup(dp: Dispatcher):
    dp.register_message_handler(welcome_commands, commands="start")
    dp.register_callback_query_handler(load_account, text='login')



