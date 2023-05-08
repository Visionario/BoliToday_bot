from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from libs.constants import photo_file
from libs.settings import AppSettings

__all__ = ['SkeletonImage']

# Settings
settings = AppSettings()


class SkeletonImage:
    """
    Draw on skeleton image
    Some code by Francisco "Cisco" Griman, https://github.com/fcoagz
    """

    def __init__(self):
        self.base_image = Image.open(Path(settings.BASE_DIR / 'res/images/skeleton.png'))
        self.draw = ImageDraw.Draw(self.base_image)
        self.font_regular = ImageFont.truetype(settings.FONT_REGULAR, size=45)
        self.font_bold = ImageFont.truetype(settings.FONT_BOLD, size=45)
        self.colors = {
                'black': (0, 0, 0),
                'white': (255, 255, 255)
                }

    def save_new_image(
            self,
            line1: str = '-',  # USD Price
            line2: str = '-',  # BTC Price
            line3: str = '-',  # Masternodes
            line4: str = '-',  # Hash Rate
            line5: str = '-',  # Difficult
            line99: str = '-',  # Last update
            ):
        """Save a new image using new values"""
        self.draw.text(xy=(300, 315), text=line1, font=self.font_bold, fill=self.colors['white'])
        self.draw.text(xy=(300, 415), text=line2, font=self.font_bold, fill=self.colors['white'])
        self.draw.text(xy=(180, 600), text=line3, font=self.font_bold, fill=self.colors['white'])
        self.draw.text(xy=(180, 700), text=line4, font=self.font_bold, fill=self.colors['white'])
        self.draw.text(xy=(180, 800), text=line5, font=self.font_bold, fill=self.colors['white'])

        self.draw.text(xy=(450, 950), text=line99, font=ImageFont.truetype(settings.FONT_REGULAR, size=30), fill=self.colors['white'])

        self.base_image.save(photo_file)  # Default tmp/ directory
