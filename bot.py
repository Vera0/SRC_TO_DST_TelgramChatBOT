import logging

import pandas
from aiogram.types import ContentType

from config import API_TOKEN
from aiogram import Bot, Dispatcher, executor, types
from config import IVCGB_CHAT_ID, MOMIAC_CHAT_ID, TRIGGER_WORDS


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def message_from_momiac(message: types.Message):
    if message.chat.id == MOMIAC_CHAT_ID:
        for i in TRIGGER_WORDS:
            if i in message.text.lower():
                await bot.forward_message(IVCGB_CHAT_ID, message.chat.id, message.message_id)
                logging.info(f"{message.date} New message from {message.from_user.full_name}")


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def message_with_doc(document: types.Document):
    if document.chat.id == MOMIAC_CHAT_ID:
        binary_doc = await bot.download_file_by_id(document.document.file_id)
        xl_file = pandas.read_excel(binary_doc)
        for i in TRIGGER_WORDS:
            if i in str(document.caption).lower() or \
                    "ивантеевская центральная городская больница" in xl_file.to_string().lower():
                await bot.forward_message(IVCGB_CHAT_ID, document.chat.id, document.message_id)
                logging.info(f"{document.date} New message with document from {document.from_user.full_name}")
            break


if __name__ == '__main__':
    executor.start_polling(dp)
