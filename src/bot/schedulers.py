# from telegram.ext import Application
#
# from bot.utils import send_new_photo_to_log
# from libs.logger import setup_logger
#
# __all__ = ['job_update_from_bolis_info', 'job_update_from_cmd']
#
# # LOGGER
# logger = setup_logger("BOT_UTILS")
#
#
# async def job_update_from_bolis_info(application: Application, *args, **kwargs):
#     """Get external_data from https://bolis.info"""
#     from datetime import datetime
#     from libs.utils import create_new_image, update_from_bolis_info
#
#     logger.debug(f'---->⌚⌚⌚⌚⌚ TICK job_update_from_bolis_info()')
#
#     update_from_bolis_info()
#
#     create_new_image(line99=f"Actualizado: {datetime.utcnow().replace(microsecond=0).isoformat()} UTC")
#
#     await send_new_photo_to_log(application=application)
#     pass
#
#
# async def job_update_from_cmd(application: Application, *args, **kwargs):
#     """Get external_data from CoinMarketCap"""
#     from datetime import datetime
#     from libs.utils import create_new_image, update_from_cmc
#
#     logger.debug(f'---->⌚⌚⌚⌚⌚ TICK job_update_from_cmd()')
#
#     update_from_cmc()
#
#     create_new_image(line99=f"Actualizado: {datetime.utcnow().replace(microsecond=0).isoformat()} UTC")
#
#     await send_new_photo_to_log(application=application)
