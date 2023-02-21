
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery

from servises.subscription_services import subscription_service
from utils.json_to_text import convert_to_text
PAYMENTS_TOKEN = "1744374395:TEST:f4ce85583f00cb94fa5e"
API_TOKEN = '5807659431:AAGOHNaS-xQQFVjzCbKeDRLe2lcfgTHy8kw'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

from servises.advertisement_services import advertisements_service
from states.advertisement_state import AdvertisementState


async def add_advertisement(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdvertisementState.name.state)
    await callback.message.answer('Введите название продукта')


async def load_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
        data['account_id'] = msg.from_user.id
        data['username'] = msg.from_user.username
    await AdvertisementState.next()
    await msg.answer('Введите описание ваших продуктов')


async def load_title(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['title'] = msg.text
    await AdvertisementState.next()
    await msg.answer('Введите цену вашего товара')


async def load_price(msg: types.Message, state=FSMContext):
    if msg.text != str:
        async with state.proxy() as data:
            data['price'] = msg.text
        await AdvertisementState.next()
        await msg.answer('Вставьте ваш юрл на товар(если у вас его нет, просто пропустите)')
    else:
        await msg.answer("Попробуйте ещё раз")

async def load_url(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['url'] = msg.text


    print(dict(data.items()))
    advertisements_service.add_advertisement(dict(data.items()))


    await state.finish()
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="go_next"))
    await msg.answer("""
    You're advertisement is saved!
    """, reply_markup=inline_kb)



async def my_advertisements(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[-1])
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    account_id = callback.from_user.id
    advertisement_list = advertisements_service.display_advertisement(account_id=account_id, page=page)
    for advertisement in advertisement_list["results"]:
        inline_kb.add(
            types.InlineKeyboardButton(f"{advertisement['id']}. {advertisement['name']}", callback_data=f"advertisement_info:{advertisement['id']}")
        )
    pagination_buttons = []

    if advertisement_list["previous"]:
        pagination_buttons.append(types.InlineKeyboardButton("⬅️", callback_data=f"show_{page - 1}"))
    if advertisement_list["next"]:
        pagination_buttons.append(types.InlineKeyboardButton("➡️", callback_data=f"show_{page + 1}"))

    inline_kb.row(*pagination_buttons).row(types.InlineKeyboardButton("Back", callback_data="go_next"))
    inline_kb.add(types.InlineKeyboardButton("Buy advertisement", callback_data="advertisement"))
    await callback.message.edit_text("Вся ваша реклама здесь!", reply_markup=inline_kb)

async def choose_purchase_method_advertisement(callback: types.CallbackQuery):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Сard", callback_data="be"))
    inline_kb.add(types.InlineKeyboardButton("Subscription", callback_data="advertisement_subscription"))
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="go_next"))
    await callback.message.edit_text("Choose purchase method", reply_markup=inline_kb)

async def subscription_check_advertisement(callback: types.CallbackQuery):
    inline_kb1 = types.InlineKeyboardMarkup(row_width=1)
    inline_kb1.add(types.InlineKeyboardButton("Сard", callback_data="be"))
    inline_kb1.add(types.InlineKeyboardButton("Buy subscription", callback_data="buy_subscription"))
    inline_kb1.add(types.InlineKeyboardButton("Back", callback_data="go_next"))

    inline_kb2 = types.InlineKeyboardMarkup(row_width=1)
    inline_kb2.add(types.InlineKeyboardButton("Place an Advertisement", callback_data="advertisement"))
    inline_kb2.add(types.InlineKeyboardButton("Description", callback_data="place_an_advertisement_description"))
    inline_kb2.add(types.InlineKeyboardButton("Back", callback_data="go_next"))
    if subscription_service.check_subscription(callback.from_user.id) != {"subscription": 0}:
        await callback.message.edit_text("Thank you for buying subscription!", reply_markup=inline_kb2)
    else:
        await callback.message.edit_text("Sorry, you need to buy subscription first, or use card.", reply_markup=inline_kb1)



async def detailed_description(query: types.CallbackQuery):
    user_id = int(query.data.split(":")[-1])
    user = advertisements_service.advertisement_info(user_id)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="go_next"))
    msg_text = convert_to_text(user)

    await query.message.edit_text(msg_text, reply_markup=inline_kb)


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(subscription_check_advertisement, Text(contains="advertisement_subscription"))
    dp.register_callback_query_handler(choose_purchase_method_advertisement, Text(contains="advertisement_purchase"))
    dp.register_callback_query_handler(detailed_description, Text(contains="advertisement_info"))
    dp.register_callback_query_handler(my_advertisements, Text(contains="show_"))
    dp.register_callback_query_handler(add_advertisement, text='advertisement')
    dp.register_message_handler(load_name, state=AdvertisementState.name)
    dp.register_message_handler(load_title, state=AdvertisementState.title)
    dp.register_message_handler(load_price, state=AdvertisementState.price)
    dp.register_message_handler(load_url, state=AdvertisementState.url)

