from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from servises.product_services import ProductService

API_TOKEN = '5807659431:AAGOHNaS-xQQFVjzCbKeDRLe2lcfgTHy8kw'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())



async def Market_Display(callback: types.CallbackQuery, state: FSMContext):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Buy Product's", callback_data="DisplayProducts_1"))
    inline_kb.add(types.InlineKeyboardButton("Place an ad", callback_data="PlaceAnAd"))
    inline_kb.add(types.InlineKeyboardButton("My Product's", callback_data="MyProducts_1"))
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="go_next"))
    await callback.message.edit_text("Пожалуйста, для уточнения тарифов обратитесь к персоналу: @todrunktodrive", reply_markup=inline_kb)


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(Market_Display, text='market_1')
