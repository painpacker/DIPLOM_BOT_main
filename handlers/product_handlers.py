from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from servises.product_services import ProductService
from states.product_state import ProductState


async def add_advertisement(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ProductState.name.state)
    await callback.message.answer('Введите название продукта')


async def load_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
        data['user_id'] = msg.from_user.id
    await ProductState.next()
    await msg.answer('Введите описание ваших продуктов')


async def load_title(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['title'] = msg.text
    await ProductState.next()
    await msg.answer('Введите цену вашего товара')


async def load_price(msg: types.Message, state=FSMContext):
    if msg.text != str:
        async with state.proxy() as data:
            data['price'] = msg.text
        await ProductState.next()
        await msg.answer('Вставьте ваш юрл на товар(если у вас его нет, просто пропустите)')
    else:
        await msg.answer("Попробуйте ещё раз")

async def load_url(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['url'] = msg.text

    print(dict(data.items()))
    ProductService.add_product(dict(data.items()))

    await state.finish()
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Activate advertisement!", callback_data="activate_advertisement"))
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="go_next"))
    await msg.answer("""
    You're advertisement is saved! But not activate, if u want to active u need to pay some price(press first button)
If u wish to return in main menu, press second button.
    """, reply_markup=inline_kb)



def setup(dp: Dispatcher):
    dp.register_callback_query_handler(add_advertisement, text='advertisement')
    dp.register_message_handler(load_name, state=ProductState.name)
    dp.register_message_handler(load_title, state=ProductState.title)
    dp.register_message_handler(load_price, state=ProductState.price)


