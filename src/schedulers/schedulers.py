from libs.logger import setup_logger
from libs.settings import AppSettings
from schedulers import bot_scheduler
from schedulers.jobs import tick_get_from_bolis_info, tick_get_from_cmd

# Settings
settings = AppSettings()

# LOGGER
logger = setup_logger("SCHEDULERS")


def add_job_tick_get_from_bolis_info():
    """Check and update data from http://bolis.info"""
    logger.info(f"Adding job: tick_get_from_bolis_info. interval:{settings.BOLIS_INFO_UPDATE_INTERVAL}")
    bot_scheduler.add_job(
            tick_get_from_bolis_info,
            'interval',
            seconds=settings.BOLIS_INFO_UPDATE_INTERVAL,
            )


def add_job_tick_get_from_cmc():
    """Check and update data from CoinMarketCap"""
    logger.info(f"Adding job: tick_get_from_cmd. interval:{settings.CMC_UPDATE_INTERVAL}")
    bot_scheduler.add_job(
            tick_get_from_cmd,
            'interval',
            seconds=settings.CMC_UPDATE_INTERVAL,
            )


def start_bot_schedulers():
    # START bot schedulers
    bot_scheduler.start()
