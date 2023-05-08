from telegram.ext import Application, ApplicationBuilder, Defaults, ExtBot

from bot_handlers import admin_handlers, basic_handlers
from libs.constants import photo_file
from libs.logger import setup_logger
from libs.settings import AppSettings
from libs.utils import do_full_update
from schedulers.schedulers import add_job_tick_get_from_bolis_info, start_bot_schedulers

# Settings
settings = AppSettings()

# LOGGER
logger = setup_logger(settings.DEFAULT_NAME)


async def post_ini(application: Application, *args, **kwargs):
    from models import Config
    logger.debug("post_ini")
    bot: ExtBot
    bot = application.bot
    await bot.send_message(
            chat_id=settings.LOG_CHANNEL,
            text=f"Initializing @{application.bot.username}"
            )
    response_photo = await bot.send_photo(
            chat_id=settings.LOG_CHANNEL,
            photo=photo_file
            )

    # Set las msg id for future message copies
    Config.set_last_photo_msg_id(response_photo.id)


async def post_stop(application: Application, *args, **kwargs):
    logger.debug("post_stop")
    await application.bot.send_message(
            chat_id=settings.LOG_CHANNEL,
            text=f"Shutting down @{application.bot.username}"
            )


def initialize():
    do_full_update()


def main():
    initialize()

    # https://docs.python-telegram-bot.org/en/stable/telegram.ext.applicationbuilder.html
    application: Application = (ApplicationBuilder()
                                .post_init(post_init=post_ini)
                                .defaults(Defaults(parse_mode='HTML'))
                                .post_stop(post_stop=post_stop)
                                .token(settings.BOT_TOKEN)
                                .build()
                                )

    # Add bot_handlers
    for h in basic_handlers:
        application.add_handler(h)

    for h in admin_handlers:
        application.add_handler(h)

    del h

    application.run_polling(drop_pending_updates=True)


add_job_tick_get_from_bolis_info()
start_bot_schedulers()

main()
