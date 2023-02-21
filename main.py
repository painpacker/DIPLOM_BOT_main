import logging
import time
import asyncio
import random
import datetime
import traceback
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram.utils import exceptions

from handlers.registration_handlers import setup as registration_handlers_setup
from handlers.advertisement_handlers import setup as advertisement_handlers_setup
from handlers.market_handlers import setup as market_handlers_setup
from handlers.welcome_handlers import setup as welcome_handlers_setup
from handlers.product_handlers import setup as product_handlers_setup
from handlers.subscription_handlers import setup as subscription_handlers_setup, days_to_seconds
from servises.advertisement_services import advertisements_service
from servises.subscription_services import subscription_service
from states.user_state import UserState
from utils.json_to_text import convert_to_text

API_TOKEN = '5807659431:AAGOHNaS-xQQFVjzCbKeDRLe2lcfgTHy8kw'
logging.basicConfig(level=logging.INFO)
Bot = Bot(token=API_TOKEN)
dp = Dispatcher(Bot, storage=MemoryStorage())

@dp.message_handler(commands='sub')
async def sub(message: types.Message, state: FSMContext):
    await state.set_state(UserState.tier.state)
    async with state.proxy() as data:
        time_sub = int(time.time()) + days_to_seconds(30)
        data['user_id'] = message.from_user.id
        subscription_service.update_user(data['user_id'], {"subscription": time_sub})
    await state.finish()
    await message.answer("Now u have subscription!")


async def send_message(user_id, message):
    try:
        await Bot.send_message(chat_id=user_id, text=message, parse_mode=ParseMode.HTML)
    except exceptions.BotBlocked:
        print(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        print(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        print(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, message)
    except exceptions.TelegramAPIError:
        print(f"Target [ID:{user_id}]: failed")


async def send_message_to_all_users(message):
    users = subscription_service.get_users()['results']
    for user_info in users:
        account_id = user_info['account_id']
        await send_message(account_id, message)

async def send_random_message_to_all_users():
    current_time = datetime.datetime.now().strftime('%H:%M')
    print(f"Current time: {current_time}")
    if current_time == '15:14':
        advertisement = advertisements_service.get_random_advertisement()
        message = (f"_______ADVERTISEMENT_______\n"
                   f"{advertisement['name']}\n"
                   f"{advertisement['title']}\n"
                   f"{advertisement['price']}\n"
                   f"{advertisement['url']}\n"
                   f"Seller: @{advertisement['username']} \n"
                   f"_______________________________")
        await send_message_to_all_users(message)

async def scheduler():
    while True:
        try:
            await send_random_message_to_all_users()
            await asyncio.sleep(60)
        except Exception as e:
            print("An error occurred in the scheduler:", e)
            traceback.print_exc()


subscription_handlers_setup(dp)
product_handlers_setup(dp)
registration_handlers_setup(dp)
advertisement_handlers_setup(dp)
market_handlers_setup(dp)
welcome_handlers_setup(dp)


print("scheduler running at", datetime.datetime.now().strftime('%H:%M:%S'))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(scheduler())
    loop.run_until_complete(executor.start_polling(dp, skip_updates=True))




