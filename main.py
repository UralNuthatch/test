import logging
import google.generativeai as genai
from aiogram import Dispatcher, Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from os import getenv
from handlers import user_handlers, other_handlers
from keyboards.set_menu import set_main_menu



BOT_TOKEN = getenv('BOT_TOKEN')
API_KEY = getenv('API_KEY')


# Настройки веб-сервера
WEB_SERVER_HOST = "https://nuthatch.onrender.com"
# Порты сервера: по умолчанию 8080
WEB_SERVER_PORT = 8080
# Путь к маршруту вебхука, по которому Telegram будет отправлять запросы
WEBHOOK_PATH = ""
# Базовый URL-адрес вебхука, который будет исп-ся для создания URL-адреса вебхука для Telegram
BASE_WEBHOOK_URL = f"{WEB_SERVER_HOST}{WEBHOOK_PATH}"
# На сервере ip4: 0.0.0.0
WEBAPP_HOST = "0.0.0.0"


bot = Bot(BOT_TOKEN)
dp = Dispatcher()


# Регистрируем роутеры в диспетчере
dp.include_router(user_handlers.router)
dp.include_router(other_handlers.router)


genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")



def main():
    # Register startup hook to initialize webhook
    dp.startup.register(on_startup)

    # Устанавливаем главное меню
    dp.startup.register(set_main_menu)

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
    logging.basicConfig(level=logging.INFO)
    main()
