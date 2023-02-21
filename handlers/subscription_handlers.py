import time

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType

from servises.subscription_services import subscription_service
from states.user_state import UserState


API_TOKEN = '5807659431:AAGOHNaS-xQQFVjzCbKeDRLe2lcfgTHy8kw'
PAYMENTS_TOKEN = "5249057655:TEST:9324b29873e388443780980ecf8d81daf3b240dfb23dd9cea50f65102ffea101"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

PRICE = types.LabeledPrice(label="Bot subscription", amount=500)


def days_to_seconds(days):
    return days*24*60*60


async def info_and_pay(callback: types.CallbackQuery):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Buy now", callback_data="buy_subscription"))
    inline_kb.add(types.InlineKeyboardButton("Back", callback_data="go_next"))
    await callback.message.edit_text("""Here you can buy a subscription that will allow you to publish ads and products for free, it's much easier and cheaper than just publish ads and products separately,\nbecause it costs only $ 5. Just buy a subscription and use our service with pleasure! """, reply_markup=inline_kb)


async def buy(callback: types.CallbackQuery):
    await bot.send_invoice(callback.message.chat.id,
                           title="Bot subscription",
                           description="subscription activate",
                           provider_token=PAYMENTS_TOKEN,
                           currency="usd",
                           photo_url="https://www.meme-arsenal.com/memes/f9e0f358b5addb31b4edd79d2783fced.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="subscription",
                           payload="test-invoice-payload")


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.SuccessfulPayment)
async def successful_payment(message: types.Message, state: FSMContext):
    await state.set_state(UserState.tier.state)
    data = await state.get_data()
    subscription_service.update_user(data["id"], {"tier": "Y"})
    await bot.send_message(message.chat.id, f"payment in the amount of  {message.successful_payment.total_amount // 100} {message.successful_payment.currency} successfully passed!")
    await state.finish()







def setup(dp: Dispatcher):
    dp.register_callback_query_handler(info_and_pay, Text(contains="info_and_pay"))
    dp.register_callback_query_handler(buy, Text(contains="buy_subscription"))


