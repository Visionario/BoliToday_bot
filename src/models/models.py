"""
Models

https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-annotated-declarative-table-type-annotated-forms-for-mapped-column
"""
import datetime
from typing import Optional

from sqlalchemy import DateTime, FetchedValue, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from libs.settings import AppSettings

__all__ = ['engine', 'Session', 'Config', 'User', ]


class Base(DeclarativeBase):
    pass


# Settings
settings = AppSettings()

engine = create_engine(
        settings.DATABASE_URI,
        echo=True,
        connect_args={"check_same_thread": False},  # For SQLite
        )

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Config(Base):
    """Bot config"""
    __tablename__ = "config"

    id: Mapped[int] = mapped_column(primary_key=True)

    bot_is_muted: Mapped[bool] = mapped_column(default=False, nullable=False)

    # From CMC
    last_usd_price: Mapped[float] = mapped_column(default=0.0, nullable=False)
    last_btc_price: Mapped[float] = mapped_column(default=0.0, nullable=False)
    last_cmc_update: Mapped[Optional[datetime.datetime]] = mapped_column(
            DateTime(timezone=True),
            default=datetime.datetime(year=2015, month=9, day=29)
            )

    # From bolis.info
    last_active_masternodes: Mapped[str] = mapped_column(default='', nullable=False)
    last_expired_masternodes: Mapped[str] = mapped_column(default='', nullable=False)
    last_hash_rate: Mapped[str] = mapped_column(default='', nullable=False)
    last_diff: Mapped[str] = mapped_column(default='', nullable=False)
    last_bolis_info_update: Mapped[Optional[datetime.datetime]] = mapped_column(
            DateTime(timezone=True),
            default=datetime.datetime(year=2015, month=9, day=29)
            )

    # Last msg id
    last_photo_msg_id: Mapped[Optional[str]] = mapped_column(default='', nullable=False)
    # Last file_id
    last_file_id: Mapped[Optional[str]] = mapped_column(default='', nullable=False)

    @classmethod
    def get_config(cls):
        with Session() as session:
            config = session.get(cls, 1)
        return config

    @classmethod
    def set_last_photo(cls, msg_id: str, file_id: str):
        """Set last msg id and file_id for future sends"""
        with Session() as session:
            config = session.get(cls, 1)
            config.last_photo_msg_id = msg_id
            config.last_file_id = file_id
            session.flush()
            session.commit()

    @classmethod
    def get_last_msg_data(cls):
        """Get last msg id and file_id"""
        with Session() as session:
            config = session.get(cls, 1)
        return (config.last_photo_msg_id, config.last_file_id)


class User(Base):
    """
        User preferences
    """

    __tablename__ = "user"

    # id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now()
            )

    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
            DateTime(timezone=True),
            # default=None,
            server_default=func.now(),
            server_onupdate=FetchedValue(),
            onupdate=func.now(),
            )

    auto_updates: Mapped[Optional[bool]] = mapped_column(default=False, nullable=False)
    language: Mapped[Optional[str]] = mapped_column(default='es', nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(default=True, nullable=False)
    last_error_tg_update: Mapped[Optional[str]] = mapped_column(String(4096))
    last_cmd: Mapped[Optional[str]] = mapped_column(String(64), default=None)


# Check or Create Database
if not settings.DATABASE_PATH.exists():
    Base.metadata.create_all(engine)
    with Session() as session:
        config = Config(
                bot_is_muted=False
                )
        session.add(config)
        session.commit()
