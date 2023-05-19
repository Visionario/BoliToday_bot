"""
Decorators
"""
from functools import wraps

from libs.settings import AppSettings
from libs.tg_users import get_or_update_user

# Settings
settings = AppSettings()


def update_to_user(func):
    """Decorator for get or create a user (user_id) and return to handler as a kwargs[user_data]"""

    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_data = get_or_update_user(update)
        if user_data is None:
            # TODO:Report error?
            pass
            return

        kwargs['user_data'] = user_data

        try:
            return await func(update, context, *args, **kwargs)
        except BaseException as e:
            print("update_to_user ERROR", e.args)

    return wrapped


def only_admins(func):
    """Decorator for: Only Admins can use this handler"""

    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in settings.ADMINS:
            print(f"Unauthorized access denied for {user_id}.")
            return
        return await func(update, context, *args, **kwargs)

    return wrapped
