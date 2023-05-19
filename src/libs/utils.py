"""
Common utils used by system
"""

from datetime import datetime, timedelta

from telegram import InputMediaPhoto, Update
from telegram.ext import Application

from libs.constants import PHOTO_FILE
from libs.external_data.api_cmc import get_cmc_data
from libs.external_data.web_scrap import BolisInfo
from libs.logger import setup_logger
from libs.settings import AppSettings
from libs.write_on_image import SkeletonImage
from models import Config, Session

__all__ = [
        'do_full_update_from_services',
        'create_new_image',
        'update_from_cmc',
        'update_from_bolis_info',
        'check_database',
        'do_full_update_from_services_if_required',
        'do_full_update_from_services',
        'send_new_photo_to_log'
        ]

# Settings
settings = AppSettings()

# LOGGER
logger = setup_logger("LIB_UTILS")


def check_database():
    """Check database asking for Config, If error HALT"""
    config: Config | None = None

    try:
        config: Config = Config.get_config()
    except BaseException as e:
        logger.critical(f"FATAL ERROR DATABASE (WILL EXIT): {e.args}")
        # TODO: report to admin/lOG before quit
        print("FATAL ERROR DATABASE:", e.args, "\nExiting...")
        exit()

    if config is None:
        logger.critical(f"FATAL ERROR DATABASE Exiting..")
        # TODO: report to admin/lOG before quit
        print("FATAL ERROR DATABASE\nExiting...")
        exit()

    return config


def update_if_required_bolis_info(config) -> bool:
    """Update from bolis.info (only if required)"""
    utc_now = datetime.utcnow()
    if (utc_now - config.last_bolis_info_update) >= timedelta(seconds=settings.BOLIS_INFO_UPDATE_INTERVAL):
        logger.debug("Updating data from bolis.info (scrapping method)")
        _ = update_from_bolis_info()
        return True

    return False


def update_if_required_cmc(config) -> bool:
    """Update from CMC (only if required)"""
    utc_now = datetime.utcnow()
    if (utc_now - config.last_cmc_update) >= timedelta(seconds=settings.CMC_UPDATE_INTERVAL):
        logger.debug("Updating data from CMC (API method)")
        _ = update_from_cmc()
        return True

    return False


async def do_full_update_from_services_if_required(update: Update):
    """Full update from services. Only if required"""
    config = check_database()
    logger.debug("Checking for full update from services if required by timedelta ...")
    if any([update_if_required_bolis_info(config), update_if_required_cmc(config)]):
        create_new_image(line99=f"Actualizado: {datetime.utcnow().replace(microsecond=0).isoformat()} UTC")
        return True

    logger.debug("Not update was required")
    return False


def do_full_update_from_services():
    """Full update from services"""

    logger.info("Doing a full update from services (Forced)...")

    config = check_database()
    update_from_bolis_info()
    update_from_cmc()
    create_new_image(line99=f"Actualizado: {datetime.utcnow().replace(microsecond=0).isoformat()} UTC")


def create_new_image(line99: str = ''):
    logger.debug("Rendering a new image...")
    config: Config = Config.get_config()

    image = SkeletonImage()
    image.save_new_image(
            line1=f"{config.last_usd_price:.8f} USD",
            line2=f"{config.last_btc_price:.8f} BTC",

            line3=f"Masternodos (Activos): {config.last_active_masternodes}",
            line4=f"Hashrate: {config.last_hash_rate}",
            line5=f"Dificultad: {config.last_diff}",
            line99=line99
            )


def update_from_cmc(save_to_db: bool = True):
    """Get updated information from CoinMarketCap and save to Database
    and return the data
    """
    error = False

    if settings.DEV_DEBUG:
        # CMC
        cmc_data_usd = {
                'status': {
                        'timestamp': '2023-05-08T02:06:35.900Z',
                        'error_code': 0,
                        'error_message': None,
                        'elapsed': 43,
                        'credit_count': 1,
                        'notice': None
                        },
                'data': {
                        '1053': {
                                'id': 1053,
                                'name': 'Bolivarcoin',
                                'symbol': 'BOLI',
                                'slug': 'bolivarcoin',
                                'num_market_pairs': 1,
                                'date_added': '2015-09-08T00:00:00.000Z',
                                'tags': ['mineable', 'pow', 'x11', 'masternodes'],
                                'max_supply': 25000000,
                                'circulating_supply': 18638951.87379985,
                                'total_supply': 18638951.87379985,
                                'is_active': 1,
                                'infinite_supply': False,
                                'platform': None,
                                'cmc_rank': 2254,
                                'is_fiat': 0,
                                'self_reported_circulating_supply': None,
                                'self_reported_market_cap': None,
                                'tvl_ratio': None,
                                'last_updated': '2023-05-08T02:05:00.000Z',
                                'quote': {
                                        'USD': {
                                                'price': 0.0028761293101173487,
                                                'volume_24h': 16.68633109,
                                                'volume_change_24h': -68.453,
                                                'percent_change_1h': -1.48030223,
                                                'percent_change_24h': -1.69805309,
                                                'percent_change_7d': -1.40338049,
                                                'percent_change_30d': 1.9423199,
                                                'percent_change_60d': 31.02612565,
                                                'percent_change_90d': -7.39873026,
                                                'market_cap': 53608.03579410243,
                                                'market_cap_dominance': 0,
                                                'fully_diluted_market_cap': 71903.23,
                                                'tvl': None,
                                                'last_updated': '2023-05-08T02:05:00.000Z'
                                                }
                                        }
                                }
                        }
                }
        cmc_data_btc = {
                'status': {
                        'timestamp': '2023-05-08T02:23:08.929Z',
                        'error_code': 0,
                        'error_message': None,
                        'elapsed': 1118,
                        'credit_count': 1,
                        'notice': None
                        },
                'data': {
                        '1053': {
                                'id': 1053,
                                'name': 'Bolivarcoin',
                                'symbol': 'BOLI',
                                'slug': 'bolivarcoin',
                                'num_market_pairs': 1,
                                'date_added': '2015-09-08T00:00:00.000Z',
                                'tags': ['mineable', 'pow', 'x11', 'masternodes'],
                                'max_supply': 25000000,
                                'circulating_supply': 18638951.87379985,
                                'total_supply': 18638951.87379985,
                                'is_active': 1,
                                'infinite_supply': False,
                                'platform': None,
                                'cmc_rank': 2254,
                                'is_fiat': 0,
                                'self_reported_circulating_supply': None,
                                'self_reported_market_cap': None,
                                'tvl_ratio': None,
                                'last_updated': '2023-05-08T02:21:00.000Z',
                                'quote': {
                                        'BTC': {
                                                'price': 1.0193167602091313e-07,
                                                'volume_24h': 0.000591646436065295,
                                                'volume_change_24h': -68.2548,
                                                'percent_change_1h': -1.02045972,
                                                'percent_change_24h': -1.19033329,
                                                'percent_change_7d': -1.31656025,
                                                'percent_change_30d': 2.22755324,
                                                'percent_change_60d': 31.3192875,
                                                'percent_change_90d': -7.06408122,
                                                'market_cap': 1.899899603769558,
                                                'market_cap_dominance': 0,
                                                'fully_diluted_market_cap': 2.5482920451695232,
                                                'tvl': None,
                                                'last_updated': '2023-05-08T02:22:00.000Z'
                                                }
                                        }
                                }
                        }
                }

    else:
        cmc_data_usd = get_cmc_data(convert_to='USD')
        cmc_data_btc = get_cmc_data(convert_to='BTC')

    if cmc_data_usd['status']['error_code'] > 0:
        usd = 0
        error = True
        # TODO: Report to admin/log?
    else:
        usd = cmc_data_usd['data']['1053']['quote']['USD']['price']

    if cmc_data_btc['status']['error_code'] > 0:
        btc = 0
        error = True
        # TODO: Report to admin/log?
    else:
        btc = cmc_data_btc['data']['1053']['quote']['BTC']['price']

    utc_now = datetime.utcnow()

    if save_to_db and not error:
        with Session() as session:
            config: Config = session.get(Config, 1)
            config.last_usd_price = usd
            config.last_btc_price = btc
            config.last_cmc_update = utc_now
            session.flush()
            logger.debug(f"Updated from CoinMarketCap")
            session.commit()

    return {'USD': usd, 'BTC': btc}


def update_from_bolis_info(save_to_db: bool = True):
    """Get updated information from https://bolis.info ; save to Database
    and return the data
    """
    bolis_info_data = BolisInfo()

    utc_now = datetime.utcnow()

    if save_to_db:
        try:
            with Session() as session:
                config: Config = session.get(Config, 1)
                config.last_active_masternodes = bolis_info_data.active_masternodes
                config.last_expired_masternodes = bolis_info_data.expired_masternodes
                config.last_hash_rate = bolis_info_data.hash_rate
                config.last_diff = bolis_info_data.difficulty
                config.last_bolis_info_update = utc_now
                session.flush()
                logger.debug(f"Updated from bolis.info")
                session.commit()
        except BaseException as e:
            pass

    return bolis_info_data


async def send_new_photo_to_log(
        application: Application | None = None,
        update: Update | None = None,
        initializing: bool = False
        ):
    from models import Config

    if application:
        # bot: ExtBot
        bot = application.bot
    elif update:
        # bot: Update
        bot = update.get_bot()
    else:
        return

    if initializing:
        logger.debug("Sending new photo to Log channel [INITIALIZING]")
        response_photo = await bot.send_photo(
                chat_id=settings.LOG_CHANNEL,
                photo=PHOTO_FILE
                )
    else:
        logger.debug("Updating photo on Log channel")
        response_photo = await bot.edit_message_media(
                chat_id=settings.LOG_CHANNEL,
                message_id=Config.get_last_msg_data()[0],
                media=InputMediaPhoto(media=open(PHOTO_FILE, 'rb')),
                )

    # Calculate best file_id
    file_id = max(((x['file_size'], x['file_id']) for x in response_photo.photo))[1]

    # Set last msg id for future message copies
    # For persistent between reboots
    Config.set_last_photo(
            msg_id=str(response_photo.id),
            file_id=str(file_id),
            )
