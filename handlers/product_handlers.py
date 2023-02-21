import time

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from servises.subscription_services import subscription_service
from utils.json_to_text import convert_to_text
PAYMENTS_TOKEN = "1744374395:TEST:f4ce85583f00cb94fa5e"
API_TOKEN = '5807659431:AAGOHNaS-xQQFVjzCbKeDRLe2lcfgTHy8kw'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

from servises.product_services import products_service
from states.product_state import ProductState


async def place_ad(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ProductState.name_2.state)
    await callback.message.answer('Enter name')


async def load_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
        data['account_id'] = msg.from_user.id
        data['username'] = msg.from_user.username
    await ProductState.next()
    await msg.answer('Enter title')


async def load_title(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['title'] = msg.text
    await ProductState.next()
    await msg.answer('Enter price')


async def load_price(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['price'] = msg.text
        await ProductState.next()
        await msg.answer("Enter you're contacts(like email or instagram or something else")

async def load_contacts(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['contacts'] = msg.text

    print(dict(data.items()))
    products_service.add_product(dict(data.items()))
    await state.finish()

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="market_1"))
    await msg.answer("""
    You're product is saved! 
    """, reply_markup=inline_kb)



async def choose_purchase_method_product(callback: types.CallbackQuery):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Сard", callback_data="be"))
    inline_kb.add(types.InlineKeyboardButton("Subscription", callback_data="product_subscription"))
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="market_1"))
    await callback.message.edit_text("Choose purchase method", reply_markup=inline_kb)

async def subscription_check_product(callback: types.CallbackQuery):
    inline_kb1 = types.InlineKeyboardMarkup(row_width=1)
    inline_kb1.add(types.InlineKeyboardButton("Сard", callback_data="be"))
    inline_kb1.add(types.InlineKeyboardButton("Buy subscription", callback_data="buy_subscription"))
    inline_kb1.add(types.InlineKeyboardButton("Back", callback_data="market_1"))

    inline_kb2 = types.InlineKeyboardMarkup(row_width=1)
    inline_kb2.add(types.InlineKeyboardButton("Place an ad", callback_data="product"))
    inline_kb2.add(types.InlineKeyboardButton("Description", callback_data="place_an_ad_description"))
    inline_kb2.add(types.InlineKeyboardButton("Back", callback_data="market_1"))
    if subscription_service.check_subscription(callback.from_user.id) != {"subscription": 0}:
        await callback.message.edit_text("Thank you for buying subscription!", reply_markup=inline_kb2)
    else:
        await callback.message.edit_text("Sorry, you need to buy subscription first, or use card.", reply_markup=inline_kb1)


async def Product_List(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[-1])
    product_response = products_service.DisplayProducts(page)
    inline_kb = types.InlineKeyboardMarkup(row_width=1)

    for product in product_response["results"]:
        inline_kb.add(
            types.InlineKeyboardButton(f"{product['name']}. {product['price']}", callback_data=f"get_product:{product['id']}")
        )

    pagination_buttons = []

    if product_response["previous"]:
        pagination_buttons.append(types.InlineKeyboardButton("⬅️", callback_data=f"DisplayProducts_{page - 1}"))
    if product_response["next"]:
        pagination_buttons.append(types.InlineKeyboardButton("➡️", callback_data=f"DisplayProducts_{page + 1}"))

    inline_kb.row(*pagination_buttons).row(types.InlineKeyboardButton("Back", callback_data="market_1"))
    await callback.message.edit_text("Welcome to our market! \nWe hope you find the product of your dreams", reply_markup=inline_kb)

async def detailed_description_of_market_products(callback: types.CallbackQuery):
    user_id = int(callback.data.split(":")[-1])
    user = products_service.get_product(user_id)
    msg = (f"{user['name']}\n"
           f"{user['title']}]\n"
           f"{user['price']}\n"
           f"Seller: @{user['username']}\n"
           f"Contacts: {user['contacts']}")

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="market_1"))

    await callback.message.edit_text(msg, reply_markup=inline_kb)



async def my_list_of_products(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[-1])
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    account_id = callback.from_user.id
    my_products = products_service.MyProducts(account_id=account_id, page=page)

    for products in my_products["results"]:
        inline_kb.add(
            types.InlineKeyboardButton(f"{products['name']}. {products['price']}", callback_data=f"get_my_products:{products['id']}")
        )
    pagination_buttons = []

    if my_products["previous"]:
        pagination_buttons.append(types.InlineKeyboardButton("⬅️", callback_data=f"MyProducts_{page - 1}"))
    if my_products["next"]:
        pagination_buttons.append(types.InlineKeyboardButton("➡️", callback_data=f"MyProducts_{page + 1}"))

    inline_kb.row(*pagination_buttons).row(types.InlineKeyboardButton("Back", callback_data="market_1"))
    inline_kb.add(types.InlineKeyboardButton("Place an ad", callback_data="PlaceAnAd"))
    await callback.message.edit_text("All you're product's are here!", reply_markup=inline_kb)


async def detailed_description_of_my_products(callback: types.CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(":")[-1])
    user = products_service.get_product(user_id)


    await state.set_state(ProductState.product.state)
    await state.update_data(user, msg_id=callback.message.message_id)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Change name", callback_data="change_name"))
    inline_kb.add(types.InlineKeyboardButton("Change title", callback_data="change_title"))
    inline_kb.add(types.InlineKeyboardButton("Change price", callback_data="change_price"))
    inline_kb.add(types.InlineKeyboardButton("Change contacts", callback_data="change_contacts"))
    inline_kb.add(types.InlineKeyboardButton("Description", callback_data="Description_1"))
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="market_1"))
    msg_text = convert_to_text(user)

    await callback.message.edit_text(msg_text, reply_markup=inline_kb)

async def name_change_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ProductState.name.state)
    msg = await callback.message.answer("Type new name")
    await state.update_data(msg_id=callback.message.message_id, msg_to_delete=msg.message_id)


async def change_username(msg: types.Message, state: FSMContext):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="market_1"))
    new_name = msg.text.strip()
    data = await state.get_data()
    product = products_service.UpdateProducts(data["id"], {"name": new_name})
    msg_text = convert_to_text(product)
    await bot.edit_message_text(msg_text, msg.chat.id, data["msg_id"], reply_markup=inline_kb)
    await bot.delete_message(msg.chat.id, data["msg_to_delete"])
    await msg.delete()
    await state.finish()

async def price_change_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ProductState.price.state)
    msg = await callback.message.answer("Type new price")
    await state.update_data(msg_id=callback.message.message_id, msg_to_delete=msg.message_id)


async def change_price(msg: types.Message, state: FSMContext):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="market_1"))
    new_price = msg.text.strip()
    data = await state.get_data()
    product = products_service.UpdateProducts(data["id"], {"price": new_price})
    msg_text = convert_to_text(product)
    await bot.edit_message_text(msg_text, msg.chat.id, data["msg_id"], reply_markup=inline_kb)
    await bot.delete_message(msg.chat.id, data["msg_to_delete"])
    await msg.delete()
    await state.finish()

async def title_change_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ProductState.title.state)
    msg = await callback.message.answer("Type new title")
    await state.update_data(msg_id=callback.message.message_id, msg_to_delete=msg.message_id)


async def change_title(msg: types.Message, state: FSMContext):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="market_1"))
    new_title = msg.text.strip()
    data = await state.get_data()
    product = products_service.UpdateProducts(data["id"], {"title": new_title})
    msg_text = convert_to_text(product)
    await bot.edit_message_text(msg_text, msg.chat.id, data["msg_id"], reply_markup=inline_kb)
    await bot.delete_message(msg.chat.id, data["msg_to_delete"])
    await msg.delete()
    await state.finish()


async def contacts_change_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ProductState.contact.state)
    msg = await callback.message.answer("Type new contacts")
    await state.update_data(msg_id=callback.message.message_id, msg_to_delete=msg.message_id)


async def change_contacts(msg: types.Message, state: FSMContext):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="market_1"))
    new_contacts = msg.text.strip()
    data = await state.get_data()
    product = products_service.UpdateProducts(data["id"], {"contacts": new_contacts})
    msg_text = convert_to_text(product)
    await bot.edit_message_text(msg_text, msg.chat.id, data["msg_id"], reply_markup=inline_kb)
    await bot.delete_message(msg.chat.id, data["msg_to_delete"])
    await msg.delete()
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(detailed_description_of_market_products, Text(contains="get_product"))
    dp.register_callback_query_handler(subscription_check_product, Text(contains="product_subscription"))
    dp.register_callback_query_handler(choose_purchase_method_product, Text(contains="PlaceAnAd"))
    dp.register_callback_query_handler(my_list_of_products, Text(contains="MyProducts_"))
    dp.register_callback_query_handler(detailed_description_of_my_products, Text(contains="get_my_products"))
    dp.register_callback_query_handler(place_ad, text="product")
    dp.register_callback_query_handler(title_change_callback, Text(contains="change_title"), state=ProductState.product)
    dp.register_message_handler(change_title, state=ProductState.title)
    dp.register_callback_query_handler(price_change_callback, Text(contains="change_price"), state=ProductState.product)
    dp.register_message_handler(change_price, state=ProductState.price)
    dp.register_callback_query_handler(name_change_callback, Text(contains="change_name"), state=ProductState.product)
    dp.register_message_handler(change_username, state=ProductState.name)
    dp.register_callback_query_handler(contacts_change_callback, Text(contains="change_contacts"), state=ProductState.product)
    dp.register_message_handler(change_contacts, state=ProductState.contact)
    dp.register_callback_query_handler(Product_List, Text(contains="DisplayProducts_"))
    dp.register_message_handler(load_name, state=ProductState.name_2)
    dp.register_message_handler(load_title, state=ProductState.title_2)
    dp.register_message_handler(load_price, state=ProductState.price_2)
    dp.register_message_handler(load_contacts, state=ProductState.contacts_2)


