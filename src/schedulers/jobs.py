from libs.logger import setup_logger
from libs.settings import AppSettings
from libs.utils import update_from_bolis_info, update_from_cmc

# Settings
settings = AppSettings()

# LOGGER
logger = setup_logger("JOBS")


def tick_get_from_bolis_info(*args, **kwargs):
    """Get external_data from https://bolis.info"""
    logger.debug(f'---->⌚⌚⌚⌚⌚ TICK tick_get_from_bolis_info()')

    update_from_bolis_info()


def tick_get_from_cmd(*args, **kwargs):
    """Get external_data from CoinMarketCap"""
    logger.debug(f'---->⌚⌚⌚⌚⌚ TICK tick_get_from_cmd()')

    update_from_cmc()
