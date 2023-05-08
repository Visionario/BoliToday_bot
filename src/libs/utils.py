from datetime import datetime, timedelta

from telegram import Update

from libs.external_data.api_cmc import get_cmc_data
from libs.external_data.web_scrap import BolisInfo
from libs.settings import AppSettings
from models import Config, Session, User
from models.pydantic import UserData

__all__ = ['get_or_update_user', 'do_full_update', 'create_new_image', 'update_from_cmc', 'update_from_bolis_info']

from libs.write_on_image import SkeletonImage

# Settings
settings = AppSettings()


def update_last_photo_file_id(file_id: str):
    """Set last file id to Config, for future sends"""


def do_full_update():
    config: Config | None = None

    # Check for database
    try:
        config: Config = Config.get_config()
    except BaseException as e:
        # TODO: report to admin/lOG before quit
        print("FATAL ERROR DATABASE:", e.args, "\nExiting...")
        exit()

    if config is None:
        # TODO: report to admin/lOG before quit
        print("FATAL ERROR DATABASE\nExiting...")
        exit()

    # Update from bolis.info
    if (datetime.now() - config.last_bolis_info_update) >= timedelta(seconds=settings.BOLIS_INFO_UPDATE_INTERVAL):
        bolis_info_data: BolisInfo = update_from_bolis_info()

    # Update from CMC
    if (datetime.now() - config.last_cmc_update) >= timedelta(seconds=settings.CMC_UPDATE_INTERVAL):
        cmc_info_data = update_from_cmc()

    #
    create_new_image(line99=f"Actualizado: {datetime.utcnow().replace(microsecond=0).isoformat()}")

    return True


def create_new_image(line99: str = ''):
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

    if save_to_db and not error:
        with Session() as session:
            config: Config = session.get(Config, 1)
            config.last_usd_price = usd
            config.last_btc_price = btc
            config.last_cmc_update = datetime.utcnow()
            session.flush()
            session.commit()

    return {'USD': usd, 'BTC': btc}


def update_from_bolis_info(save_to_db: bool = True):
    """Get updated information from https://bolis.info and save to Database
    and return the data
    """
    bolis_info_data = BolisInfo()

    if save_to_db:
        with Session() as session:
            config: Config = session.get(Config, 1)
            config.last_active_masternodes = bolis_info_data.active_masternodes
            config.last_expired_masternodes = bolis_info_data.expired_masternodes
            config.last_hash_rate = bolis_info_data.hash_rate
            config.last_diff = bolis_info_data.difficulty
            config.last_bolis_info_data_update = datetime.utcnow()
            session.flush()
            session.commit()

    return bolis_info_data


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
