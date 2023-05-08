from db.helpers import create_tables
from db.models import Config, Session

create_tables(i_am_sure=True)

with Session() as session:
    config = Config(
            bot_is_muted=False
            )
    session.add(config)
    session.commit()
