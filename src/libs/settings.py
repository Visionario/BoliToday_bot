"""
System Settings
"""
import os
from pathlib import Path

from dotenv import load_dotenv

from libs.constants import APP_VERSION, DATABASE_FILE

__all__ = ['AppSettings']


class AppSettings(object):
    """App settings reading on realtime from '.env' file.

        Use: settings = AppSettings()
    """
    __slots__ = (
            'BASE_DIR',
            'DEFAULT_NAME',
            'DEFAULT_UTILITY_NAME',
            'DEV_DEBUG',
            'LOG_FILE',
            'LOG_LEVEL',
            'BOT_TOKEN',
            'DATABASE_URI',
            'DATABASE_PATH',
            'ADMINS',
            'LOG_CHANNEL',
            'CMC_PRO_API_KEY',

            'CMC_UPDATE_INTERVAL',
            'BOLIS_INFO_UPDATE_INTERVAL',

            'NOTIFY_STARTUP',
            'NOTIFY_SHUTDOWN',

            'FONT_REGULAR',
            'FONT_BOLD',
            'FONT_EXTRA_BOLD',
            'FONT_BLACK',

            'APP_INFO',
            )

    def __init__(self, initializing=False, *args, **kwargs):
        DEFAULT_NAME = "BoliToday_bot"

        # Read all variable environments
        load_dotenv()

        # BASE_DIR is exactly when source is, avoid bad references when importing
        self.BASE_DIR = Path(__file__).resolve().parent.parent

        self.DEFAULT_NAME = DEFAULT_NAME

        # Telegram credentials
        self.BOT_TOKEN = str(os.getenv('BOLITODAY_BOT_TOKEN', ''))
        if not self.BOT_TOKEN and not initializing:
            print("WARNING: NO BOT_TOKEN DECLARED. Please check environments settings for 'BOLITODAY_BOT_TOKEN'. Exiting...")
            exit()

        # Bot Admins
        self.ADMINS = [int(a) for a in str(os.getenv('BOLITODAY_ADMINS', '0')).split(',')]
        if not self.ADMINS and not initializing:
            print("WARNING: NO ADMINS DECLARED. Please check environments settings for 'BOLITODAY_ADMINS'. Exiting..")
            exit()

        # Log channel
        self.LOG_CHANNEL = int(os.getenv('BOLITODAY_LOG_CHANNEL', 0))
        if self.LOG_CHANNEL == 0 and not initializing:
            # Set log channel to first Admin in ADMINS list
            self.LOG_CHANNEL = self.ADMINS[0]

        # CoinMarketCap API KEY
        self.CMC_PRO_API_KEY = str(os.getenv('BOLITODAY_CMC_PRO_API_KEY', ''))
        if not self.CMC_PRO_API_KEY and not initializing:
            print("WARNING: NO CMC_PRO_API_KEY FOUND. Please check environments settings for 'BOLITODAY_CMC_PRO_API_KEY'. Exiting..")
            exit()

        # Intervals for Updates
        self.CMC_UPDATE_INTERVAL = int(os.getenv('CMC_UPDATE_INTERVAL', 900))

        self.BOLIS_INFO_UPDATE_INTERVAL = int(os.getenv('BOLITODAY_BOLIS_INFO_UPDATE_INTERVAL', 300))

        # Force lowercase and NO spaces
        self.DEFAULT_UTILITY_NAME = DEFAULT_NAME.strip().replace(" ", "_").lower()

        self.DEV_DEBUG = bool(os.getenv('BOLITODAY_DEV_DEBUG', False))

        # Log settings
        # test/create Logs dir
        Path(self.BASE_DIR / 'logs').mkdir(exist_ok=True)
        self.LOG_FILE = Path(self.BASE_DIR / 'logs' / f"{DEFAULT_NAME.lower()}.log")
        self.LOG_LEVEL = str(os.getenv('BOLITODAY_LOG_LEVEL', 'INFO'))

        # Database (SQLite by default)
        self.DATABASE_URI = str(os.getenv('BOLITODAY_DATABASE_URI', f'sqlite:///database/{DATABASE_FILE}'))
        self.DATABASE_PATH = Path(self.BASE_DIR / 'database' / DATABASE_FILE)

        # Notifications
        self.NOTIFY_STARTUP = bool(os.getenv('BOLITODAY_NOTIFY_STARTUP', False))
        self.NOTIFY_SHUTDOWN = bool(os.getenv('BOLITODAY_NOTIFY_STARTUP', False))

        # Fonts
        self.FONT_REGULAR = Path(self.BASE_DIR / 'res/fonts' / str(os.getenv('BOLITODAY_FONT_REGULAR', 'Orbitron-Regular.ttf'))).as_posix()
        self.FONT_BOLD = Path(self.BASE_DIR / 'res/fonts' / str(os.getenv('BOLITODAY_FONT_BOLD', 'Orbitron-Bold.ttf'))).as_posix()
        self.FONT_EXTRA_BOLD = Path(self.BASE_DIR / 'res/fonts' / str(os.getenv('BOLITODAY_FONT_EXTRA_BOLD', 'Orbitron-ExtraBold.ttf'))).as_posix()
        self.FONT_BLACK = Path(self.BASE_DIR / 'res/fonts' / str(os.getenv('BOLITODAY_FONT_BLACK', 'Orbitron-Black.ttf'))).as_posix()

        # App data info
        self.APP_INFO = {
                'name': DEFAULT_NAME,
                'license': "GPL-3",
                'version': APP_VERSION,
                'status': "DEVELOPMENT",
                'author': "Asdrúbal Velásquez Lagrave",
                'contact': "Telegram/Twitter/Github: @Visionario",
                'author_tg': "@Visionario",
                'credits': ["Asdrúbal Velásquez Lagrave", ],
                'maintainer': "Asdrúbal Velásquez Lagrave",
                }
