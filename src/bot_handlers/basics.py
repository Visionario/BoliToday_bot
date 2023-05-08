from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

from libs.decorators import update_to_user
from libs.logger import setup_logger
from libs.responses import responses_es
from libs.settings import AppSettings

# Settings
settings = AppSettings()

# LOGGER
logger = setup_logger("HANDLERS_BASICS")
# logger = setup_logger(__name__)

__all__ = ['basic_handlers']


@update_to_user
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
    logger.debug("handler_start")
    user_data = kwargs['user_data']

    if user_data.created:
        msg = responses_es.get('menu_start_new_user').replace('{{first_name}}', update.effective_chat.first_name)
    else:
        msg = responses_es.get('menu_start_returning_user').replace('{{first_name}}', update.effective_chat.first_name)

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=msg
            )


@update_to_user
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
    logger.debug("handler_price")
    user_data = kwargs['user_data']

    from models import Config
    await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            message_id=Config.get_last_msg_id(),
            from_chat_id=settings.LOG_CHANNEL,
            )


# Manage bot handlers
basic_handlers = list()
basic_handlers.append(
        CommandHandler(
                command=['start', 'iniciar'],
                callback=start,
                filters=filters.ChatType.PRIVATE
                )
        )
basic_handlers.append(
        CommandHandler(
                ['price', 'precio'],
                callback=price,
                filters=filters.ChatType.PRIVATE
                )
        )
