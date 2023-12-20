import google.generativeai as genai
from aiogram import Dispatcher, Bot
from aiogram.types import Message
from os import getenv


BOT_TOKEN = getenv('BOT_TOKEN')
API_KEY = getenv('API_KEY')

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')


@dp.message()
async def get_send_text(message: Message):
    try:
        responce = model.generate_content(message.text)
        await message.answer(responce.text)
    except Exception as ex:
        await message.answer("Error")


if __name__ == '__main__':
    dp.run_polling(bot)
