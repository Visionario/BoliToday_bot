from datetime import datetime

from pydantic import BaseModel


class UserData(BaseModel):
    """UserData"""
    user_id: int
    created_at: datetime
    updated_at: datetime
    auto_updates: bool
    language: str
    is_active: bool
    last_error_tg_update: str | None = None
    last_cmd: str | None = None
    created: bool = False
