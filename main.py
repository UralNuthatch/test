import google.generativeai as genai
from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from os import getenv



# Настройки веб-сервера
WEB_SERVER_HOST = "https://nuthatch.onrender.com"
# Порты сервера: 8300-8499
WEB_SERVER_PORT = "8350"
# Путь к маршруту вебхука, по которому Telegram будет отправлять запросы
WEBHOOK_PATH = ""
# Базовый URL-адрес вебхука, который будет исп-ся для создания URL-адреса вебхука для Telegram
BASE_WEBHOOK_URL = f"{WEB_SERVER_HOST}{WEBHOOK_PATH}"
# На сервере только IPv6 (аналог ip4: 0.0.0.0)
WEBAPP_HOST = "::"


BOT_TOKEN = getenv('BOT_TOKEN')
API_KEY = getenv('API_KEY')

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")

@dp.message(CommandStart)
async def get_process_start(message: Message):
    await message.answer("Start been activated. Hello!")


@dp.message()
async def get_send_text(message: Message):
    try:
        responce = model.generate_content(message.text)
        await message.answer(responce.text)
    except Exception as ex:
        await message.answer("Error")


def main():
    # Register startup hook to initialize webhook
    dp.startup.register(on_startup)

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Create an instance of request handler
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )

    # Register webhook handler on application
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # Запускаем веб-сервер
    web.run_app(app, host=WEBAPP_HOST)



if __name__ == '__main__':
    main()
