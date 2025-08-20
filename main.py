
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('TOKEN')

logger.info("TOKEN is " + BOT_TOKEN)

WEBHOOK_URL = os.getenv("WEBHOOK") + '/webhook'

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def cmd_start(message: types.Message):
    logger.info(str(message.new_chat_members) + ' ' + str(message.left_chat_member))
    if message.new_chat_members is None and message.left_chat_member is None:
        return
    logger.info("Removing message!!! chat id is " + str(message.chat.id))
    await message.delete()

async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)
    logger.info("Bot started with webhook: " + WEBHOOK_URL)

async def on_shutdown(bot: Bot):
    logger.info("shutting down webhook")
    await bot.delete_webhook()

async def handle_root(_: web.Request):
    return web.Response(text="Hey cool to see you")

async def main():
    app = web.Application()

    app.add_routes([
        web.get('/', handle_root)
    ])

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path='/webhook')

    setup_application(app, dp, bot=bot)
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    logger.info("Starting webhook")
    return app

if __name__ == "__main__":
    web.run_app(main(), host="0.0.0.0", port=9990)
