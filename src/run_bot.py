from libs.logger import setup_logger
from libs.settings import AppSettings
from libs.utils import do_full_update_from_services

# Settings
settings = AppSettings()

# LOGGER
logger = setup_logger(settings.DEFAULT_NAME)


def _initialize():
    do_full_update_from_services()


def main():
    from bot.utils import build_tg_app

    app = build_tg_app()
    # job_queue = app.job_queue

    # logger.info("Preparing jobs and schedulers for automatic tasks...")

    # logger.info(f"Updating from bolis.info (scrapper mode), every {settings.BOLIS_INFO_UPDATE_INTERVAL} seconds")
    # job_repeating_update_from_bolis_info = job_queue.run_repeating(
    #         callback=job_update_from_bolis_info,
    #         interval=settings.BOLIS_INFO_UPDATE_INTERVAL,
    #         name='job_repeating_update_from_bolis_info',
    #         )
    # logger.info(f"Updating from CoinMarketCap via API every {settings.CMC_UPDATE_INTERVAL} seconds")
    # job_repeating_update_from_cmc = job_queue.run_repeating(
    #         callback=job_update_from_cmd,
    #         interval=settings.CMC_UPDATE_INTERVAL,
    #         name='job_repeating_update_from_cmc',
    #         )

    app.run_polling()


if __name__ == '__main__':
    logger.info("Initializing ...")
    _initialize()

    main()
