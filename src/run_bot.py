from telegram.ext import Application, ApplicationBuilder, Defaults, ExtBot

from bot_handlers import admin_handlers, basic_handlers
from libs.constants import PHOTO_FILE
from libs.logger import setup_logger
from libs.settings import AppSettings
from libs.utils import do_full_update
from schedulers.schedulers import add_job_tick_get_from_bolis_info, add_job_tick_get_from_cmc, start_bot_schedulers

# Settings
settings = AppSettings()

# LOGGER
logger = setup_logger(settings.DEFAULT_NAME)


async def post_ini(application: Application, *args, **kwargs):
    from models import Config
    logger.info("post_ini")

    bot: ExtBot
    bot = application.bot

    # IGNORE THIS--> if settings.NOTIFY_STARTUP:
    logger.info("Sending telegram notify to log channel for Startup")
    await bot.send_message(
            chat_id=settings.LOG_CHANNEL,
            text=f"Initializing @{application.bot.username}, Ver:{settings.APP_INFO['version']}"
            )

    response_photo = await bot.send_photo(
            chat_id=settings.LOG_CHANNEL,
            photo=PHOTO_FILE
            )

    # Set las msg id for future message copies
    Config.set_last_photo_msg_id(response_photo.id)


async def post_stop(application: Application, *args, **kwargs):
    logger.info("post_stop")

    if settings.NOTIFY_SHUTDOWN:
        logger.info("Sending telegram notify to log channel for Shutdown")
        await application.bot.send_message(
                chat_id=settings.LOG_CHANNEL,
                text=f"Shutting down @{application.bot.username}"
                )


def add_handlers(application: Application):
    """Add bot handlers"""
    logger.info("Adding Telegram Bot handlers ...")

    for handler in basic_handlers:
        logger.info(f"Handler for {handler.commands}")
        application.add_handler(handler)

    for handler in admin_handlers:
        logger.info(f"Handler for {handler.commands}")
        application.add_handler(handler)


def initialize():
    do_full_update()


def main():
    logger.info("Initializing ...")
    initialize()

    # https://docs.python-telegram-bot.org/en/stable/telegram.ext.applicationbuilder.html
    logger.info("Building Telegram Bot ...")
    application: Application = (ApplicationBuilder()
                                .post_init(post_init=post_ini)
                                .defaults(Defaults(parse_mode='HTML'))
                                .post_stop(post_stop=post_stop)
                                .token(settings.BOT_TOKEN)
                                .build()
                                )

    add_handlers(application)

    logger.info("Entering in polling mode...")
    application.run_polling(drop_pending_updates=True)


logger.info("Preparing jobs and schedulers for automatic tasks...")
add_job_tick_get_from_bolis_info()
add_job_tick_get_from_cmc()
start_bot_schedulers()

main()
