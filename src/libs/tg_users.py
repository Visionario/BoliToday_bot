from telegram import Update

from models import Session, User
from models.pydantic import UserData


def get_or_update_user(update: Update):
    """
    Get or Create a user. Using data from update.
    if error return None

    """
    created = False

    with Session() as session:
        user: User = session.get(User, update.effective_chat.id)

        if user is None:
            user = User(
                    user_id=update.effective_chat.id,
                    # updated_at=update.message.date
                    )
            session.add(user)
            session.flush()
            created = True
        else:
            user.is_active = True
            user.last_cmd = update.message.text
            user.updated_at = update.message.date

        try:
            user_data = UserData(
                    user_id=user.user_id,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                    auto_updates=user.auto_updates,
                    language=user.language,
                    is_active=user.is_active,
                    last_error_tg_update=user.last_error_tg_update,
                    created=created
                    )

            session.commit()
        except BaseException as e:
            print("get_or_update_user ERROR", e.args)
            session.rollback()
            return None
    return user_data
