from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import CommandHandler, ContextTypes, filters

from libs.decorators import update_to_user
from libs.logger import setup_logger
from libs.responses import responses_es
from libs.settings import AppSettings
from libs.utils import do_full_update_from_services_if_required, send_new_photo_to_log
from models import Config

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
async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
    user_data = kwargs['user_data']
    logger.debug(
            f"Sending data for user_id:{update.effective_user.id} username: @{update.effective_user.username} first_name:{update.effective_user.first_name}"
            )

    await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
            )

    updated = await do_full_update_from_services_if_required(update=update)
    if updated:
        await send_new_photo_to_log(update=update)

    await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=Config.get_last_msg_data()[1]
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
                callback=get_price,
                filters=filters.ChatType.PRIVATE
                )
        )
