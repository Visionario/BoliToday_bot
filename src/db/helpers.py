from pathlib import Path

from db import engine
from db.models import Base


def create_tables(i_am_sure=False):
    if not i_am_sure:
        print("Param: i_am_sure must be True to create tables ")
        return

    # Delete old database (sqlite) if exist
    Path("database.sqlite3").unlink(missing_ok=True)

    try:
        Base.metadata.drop_all(engine)
    except:
        pass

    Base.metadata.create_all(engine)
