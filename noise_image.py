from enum import Enum, auto

import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


class Color(Enum):
    """2D画像をカラーで作成するかモノクロで作成するかの指定を行う列挙型。"""

    MONO = 1  # モノクロ
    RGB = 3  # RGBカラー


class NoiseImage:
    """乱数を使用した2Dのノイズ画像を生成する"""

    COLOR = ("rgb", "mono")  # RGB画像かモノクロか

    def __init__(
        self, width=512, height=512, mag=1, color: Color = Color.RGB, resumple=Image.BOX
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
        self.orig_w = width
        self.orig_h = height
        self.mag = mag
        self.width = width * mag
        self.height = height * mag
        self.color = color
        self.resumple = resumple
        rimage = np.random.randint(
            0, 256, (self.orig_h, self.orig_w, self.color.value)
        ).astype(np.uint8)
        src_img = Image.fromarray(rimage)
        self.img = src_img.resize((self.width, self.height), resample=self.resumple)
