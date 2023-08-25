from enum import Enum, auto
import numpy as np
from PIL import Image


class Color(Enum):
    """2D画像をカラーで作成するかモノクロで作成するかの指定を行う列挙型。"""

    MONO = 1    # モノクロ
    RGB = 3     # RGBカラー


class NoiseImage:
    """乱数を使用した2Dのノイズ画像を生成する"""

    def __init__(
        self, width=512, height=512, mag=1,
        color: Color = Color.RGB, resample: int=Image.BOX
    ) -> None:
        """カラーもしくはモノクロで2Dのノイズ画像を生成して初期化。
        指定されたサイズで画像を生成後、指定された拡大方法、拡大率で拡大を行う。
        Args:
            width(int): 画像の幅。
            height(int): 画像の高さ。
            mag(int): 拡大率。
            color(Color): カラーかモノクロかの指定。
            resumple: 拡大方法。Imageクラスの拡大方法を指定。
        """
        self._orig_w = width
        self._orig_h = height
        self._mag = mag
        self._width = width * mag
        self._height = height * mag
        self._color = color
        self._resample = resample
        rimage = np.random.randint(0, 256, (self._orig_h, self._orig_w, 3)) \
            if self._color == Color.RGB \
                else np.random.randint(0, 256, (self._orig_h, self._orig_w))
        src_img = Image.fromarray(rimage.astype(np.uint8))
        self._image = src_img.resize((self._width, self._height),
                                     resample=self._resample) # type: ignore

    @property
    def image(self):
        return self._image
