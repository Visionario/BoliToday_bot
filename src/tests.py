from models import *

with Session() as session:
    user = User(user_id=123)
    session.add(user)
    session.commit()
