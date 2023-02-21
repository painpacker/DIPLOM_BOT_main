from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
API_TOKEN = '5807659431:AAGOHNaS-xQQFVjzCbKeDRLe2lcfgTHy8kw'
PAYMENTS_TOKEN = "1744374395:TEST:f4ce85583f00cb94fa5e"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.callback_query_handler(Text(contains="go_next"))
async def user_is_registered(callback: types.CallbackQuery):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Advertisement", callback_data="advertisement_purchase"))
    inline_kb.add(types.InlineKeyboardButton("My advertisement", callback_data="show_1"))
    inline_kb.add(types.InlineKeyboardButton("Market", callback_data="market_1"))
    inline_kb.add(types.InlineKeyboardButton("Subscription", callback_data="info_and_pay"))
    await callback.message.edit_text(f"Hello {callback.from_user.username}", reply_markup=inline_kb)


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(user_is_registered, text="go_next")
