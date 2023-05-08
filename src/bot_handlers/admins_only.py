from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

from libs.decorators import only_admins
from libs.logger import setup_logger
from libs.settings import AppSettings
from models import Config, Session

# Settings
settings = AppSettings()

# LOGGER
logger = setup_logger("HANDLERS_ADMINS")
# logger = setup_logger(__name__)

__all__ = ['admin_handlers']


@only_admins
async def mode_mute(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
    """Mute/Unmute Bot: Ignore all users except ADMINS"""
    logger.debug("mode_mute")

    # new_value = db_update(Config).where(Config.c.id == 1).values(bot_is_muted=True)

    mute_switch = update.message.text.lower().split(' ')[-1:][0]
    if mute_switch == 'on':
        mute_switch = True
    else:
        mute_switch = False

    with Session() as session:
        config = session.get(Config, 1)
        config.bot_is_muted = mute_switch
        session.commit()

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Bot is: {'<code>muted</code>' if mute_switch else '<code>NOT muted</code>'}"
            )


# Manage bot handlers
admin_handlers = list()
admin_handlers.append(
        CommandHandler(
                command=['mute'],
                callback=mode_mute,
                filters=filters.ChatType.PRIVATE
                )
        )
