from telegram.ext import Application, ApplicationBuilder, Defaults, ExtBot

from bot.handlers import admin_handlers, basic_handlers
from libs.logger import setup_logger
from libs.settings import AppSettings
from libs.utils import send_new_photo_to_log

__all__ = ['build_tg_app', 'send_new_photo_to_log']

# Settings
settings = AppSettings()

# LOGGER
logger = setup_logger("BOT_UTILS")


async def _post_ini(application: Application):
    logger.info("_post_ini")

    bot: ExtBot
    bot = application.bot

    logger.info("Sending telegram notify to log channel for Startup")
    await bot.send_message(
            chat_id=settings.LOG_CHANNEL,
            text=f"Initializing @{application.bot.username}, Ver:{settings.APP_INFO['version']}"
            )

    await send_new_photo_to_log(application=application, initializing=True)


async def _post_stop(application: Application):
    logger.info("_post_stop")

    if settings.NOTIFY_SHUTDOWN:
        logger.info("Sending telegram notify to log channel for Shutdown")
        await application.bot.send_message(
                chat_id=settings.LOG_CHANNEL,
                text=f"Shutting down @{application.bot.username}"
                )


def _add_handlers(application: Application):
    """Add bot handlers defined in handlers package"""
    logger.info("Adding Telegram Bot handlers ...")

    for handler in basic_handlers:
        logger.info(f"Handler for {handler.commands}")
        application.add_handler(handler)

    for handler in admin_handlers:
        logger.info(f"Handler for {handler.commands}")
        application.add_handler(handler)


def build_tg_app():
    logger.info("Building Telegram Bot ...")

    application: Application = (ApplicationBuilder()
                                .post_init(post_init=_post_ini)
                                .defaults(Defaults(parse_mode='HTML'))
                                .post_stop(post_stop=_post_stop)
                                .token(settings.BOT_TOKEN)
                                .build()
                                )

    _add_handlers(application)

    return application
