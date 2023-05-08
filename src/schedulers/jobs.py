from datetime import datetime

from libs.logger import setup_logger
from libs.settings import AppSettings
from libs.utils import create_new_image

# Settings
settings = AppSettings()

# LOGGER
logger = setup_logger("JOBS")


def tick_get_from_bolis_info(*args, **kwargs):
    """Get external_data from https://bolis.info"""
    logger.debug(f'---->⌚⌚⌚⌚⌚ TICK tick_get_from_bolis_info()\n{kwargs}\n')

    logger.debug(f'Create a new image using Config data saved from others ticks')

    create_new_image(line99=f"Actualizado: {datetime.utcnow().replace(microsecond=0).isoformat()}")
