#
# import asyncio
# import datetime
# import random
#
# from aiogram import Bot
# from aiogram.types import ParseMode
# from aiogram.utils import exceptions
#
# from servises.advertisement_services import advertisements_service
# from servises.subscription_services import subscription_service
#
#
# async def send_message(user_id, message):
#     try:
#         await Bot.send_message(chat_id=user_id, text=message, parse_mode=ParseMode.HTML)
#     except exceptions.BotBlocked:
#         print(f"Target [ID:{user_id}]: blocked by user")
#     except exceptions.ChatNotFound:
#         print(f"Target [ID:{user_id}]: invalid user ID")
#     except exceptions.RetryAfter as e:
#         print(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
#         await asyncio.sleep(e.timeout)
#         return await send_message(user_id, message)
#     except exceptions.TelegramAPIError:
#         print(f"Target [ID:{user_id}]: failed")

#
# async def send_message_to_all_users(message):
#     users = subscription_service.get_users()
#     for user in users:
#         user_id = user['account_id']
#         await send_message(user_id, message)
#
#
# async def send_random_message_to_all_users():
#     current_time = datetime.datetime.now().strftime('%H:%M')
#     print(f"Current time: {current_time}")
#     if current_time == '17:36':
#         response = advertisements_service.all_advertisement()
#         messages = response.json()
#         message = random.choice(messages)
#         await send_message_to_all_users(message)
#
#
# async def scheduler():
#     while True:
#         await send_random_message_to_all_users()
#         await asyncio.sleep(60)




