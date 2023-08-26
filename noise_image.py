from enum import Enum
import numpy as np
from PIL import Image


class Color(Enum):
    """2D画像をカラーで作成するかモノクロで作成するかの指定を行う列挙型。"""

    MONO = 1  # モノクロ
    RGB = 3  # RGBカラー


class NoiseImage:
    """乱数を使用した2Dのノイズ画像を生成するクラス"""

    def __init__(
        self,
        width=512,
        height=512,
        #        mag=1,
        color=Color.RGB,
        #        resample=Image.BOX,
        seed=-1,
    ) -> None:
        """カラーもしくはモノクロで2Dのノイズ画像を生成するためのパラメーターを初期化。
        Args:
            width(int): 画像の幅。16ピクセル以上。
            height(int): 画像の高さ。16ピクセル以上。
            color(Color): カラーかモノクロかの指定。
            seed(int): 乱数発生のシード値。0もしくは負数は自動設定。
        Raises:
            ValueError: 画像サイズが小さい場合。
        """
        if (width <= 16) or (height <= 16):
            raise ValueError
        self._width = width
        self._height = height
        self._color = color
        if seed <= 0:
            np.random.seed()
        else:
            np.random.seed(seed)
        rimage = (
            np.random.randint(0, 256, (height, width, 3))
            if self._color == Color.RGB
            else np.random.randint(0, 256, (height, width))
        )
        self._image = Image.fromarray(rimage.astype(np.uint8))

    @property
    def image(self):
        return self._image

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def color(self):
        return self._color

    def enlarge(self, mag=1, resample=Image.BOX):
        """画像の拡大を行う。
        Args:
            mag(int): 拡大率。
            resample: 拡大方法。Imageクラスの拡大方法を指定。
        Returns:
            Image: 拡大後の画像。
        Raises:
            ValueError: 拡大率が0もしくは負数の場合。
        """
        if mag <= 0:
            raise ValueError
        self._width *= mag
        self._height *= mag
        self._image = self._image.resize(
            (self._width, self._height), resample=resample  # type: ignore
        )
        return self._image

    def __add__(self, other):
        '''+演算子。画像を重ね合わせる。
        Args:
            other(NoiseImage): 重ね合わせる画像。
        Returns:
            重ね合わせた後の画像。
        Raises:
            TypeError: 重ね合わせる画像の型が合わない。
            ValueError: 重ね合わせる画像のサイズが合わない。
        '''
        if type(other) != NoiseImage:
            raise TypeError
        if self._image.size != other.image.size:
            raise ValueError
        return Image.blend(self._image, other.image, 0.5)

    def __iadd_(self, other):
        '''+=演算子。画像を重ね合わせる。
        Args:
            other(NoiseImage): 重ね合わせる画像。
        Returns:
            重ね合わせた後の画像。
        Raises:
            TypeError: 重ね合わせる画像の型が合わない。
            ValueError: 重ね合わせる画像のサイズが合わない。
        '''
        self = self + other
        return self