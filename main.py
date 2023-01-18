import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import User, CallbackQuery

from handlers.registration_handlers import setup as registration_handlers_setup
from handlers.advertisement_handlers import setup as advertisement_handlers_setup
from servises.advertisement_servises import advertisements_service

API_TOKEN = '5807659431:AAGOHNaS-xQQFVjzCbKeDRLe2lcfgTHy8kw'

logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"])
async def welcome_comands(msg: types.Message):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Registration", callback_data="registration_1"))
    await msg.answer(f"You're Welcome!, u're id is {msg.from_user.id}", reply_markup=inline_kb)

@dp.callback_query_handler(Text(contains="go_next"))
async def user_is_registered(callback: types.CallbackQuery):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Advertisement", callback_data="advertisement"))
    inline_kb.add(types.InlineKeyboardButton("My advertisement", callback_data="MyAdvertisement"))
    inline_kb.add(types.InlineKeyboardButton("Market", callback_data="market_1"))
    inline_kb.add(types.InlineKeyboardButton("Balance", callback_data="balance"))
    inline_kb.add(types.InlineKeyboardButton("Subscription", callback_data="subscription"))
    await callback.message.edit_text("You're Welcome!", reply_markup=inline_kb)


@dp.callback_query_handler(Text(contains="MyAdvertisement"))
async def my_advertisements(query: CallbackQuery):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    user_id = query.from_user.id
    advertisement_list = advertisements_service.my_advertisement(user_id=user_id)
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="go_next"))
    # for advertisement in advertisement_list["results"]:
    #     inline_kb.add(
    #         types.InlineKeyboardButton(f"{advertisement['title']}. {advertisement['name']}")
    #     )
    await query.message.edit_text(advertisement_list, reply_markup=inline_kb)




@dp.callback_query_handler(Text(contains="market_1"))
async def Market_Display(callback: types.CallbackQuery):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Buy Product's", callback_data="BuyProducts"))
    inline_kb.add(types.InlineKeyboardButton("Place an ad", callback_data="PlaceAnAd"))
    inline_kb.add(types.InlineKeyboardButton("My Product's", callback_data="MyProducts"))
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="go_next"))
    await callback.message.edit_text("Пожалуйста, для уточнения тарифов обратитесь к персоналу: @todrunktodrive", reply_markup=inline_kb)


registration_handlers_setup(dp)
advertisement_handlers_setup(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

c