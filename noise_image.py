from enum import Enum
import sys
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
        color=Color.RGB,
        seed=-1,
    ) -> None:
        """カラーもしくはモノクロで2Dのノイズ画像を生成するためのパラメーターを初期化。
        Args:
            width(int): 画像の幅。16ピクセル以上で16の倍数。
            height(int): 画像の高さ。16ピクセル以上で16の倍数。
            color(Color): カラーかモノクロかの指定。
            seed(int): 乱数発生のシード値。0もしくは負数は自動設定。
        Raises:
            ValueError: 画像サイズが条件に合わない場合。
        """
        if (width < 16) or (height < 16) or (width % 16 != 0) or (height % 16 != 0):
            raise ValueError("画像サイズは16x16以上で16の倍数として下さい。")
        self.__width = width
        self.__height = height
        self.__color = color
        np.random.seed()
        self.__seed = seed if seed > 0 else np.random.randint(1, np.iinfo(np.int32).max)
        # np.random.seed(self.__seed)
        self.__image: Image.Image | None = None
        # rimage = (
        #     np.random.randint(0, 256, (height, width, 3))
        #     if self._color == Color.RGB
        #     else np.random.randint(0, 256, (height, width))
        # )
        # self._image = Image.fromarray(rimage.astype(np.uint8))

    @property
    def image(self) -> Image.Image | None:
        return self.__image

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def color(self) -> Color:
        return self.__color

    @property
    def seed(self) -> int:
        return self.__seed

    @width.setter
    def width(self, value: int):
        if (value < 16) or (value % 16 != 0):
            raise ValueError("画像の幅は16以上で16の倍数として下さい。")
        self.__width = value

    @height.setter
    def height(self, value: int):
        if (value < 16) or (value % 16 != 0):
            raise ValueError("画像の高さは16以上で16の倍数として下さい。")
        self.__height

    @color.setter
    def color(self, value: Color):
        self.__color = value

    @seed.setter
    def seed(self, value: int):
        if value > 0:
            self.__seed = value
        else:
            np.random.seed()
            self.__seed = np.random.randint(1, np.iinfo(np.int32).max)

    @image.setter
    def image(self, value: Image.Image | None):
        self.__image = value

    # def enlarge(self, mag=1, resample=Image.NONE):
    #     """画像の拡大を行う。
    #     Args:
    #         mag(int): 拡大率。
    #         resample: 拡大方法。Imageクラスの拡大方法を指定。
    #     Returns:
    #         Image: 拡大後の画像。
    #     Raises:
    #         ValueError: 拡大率が0もしくは負数の場合か、拡大方法の指定が誤り。
    #     """
    #     if mag <= 0:
    #         raise ValueError
    #     if resample is Image.NONE:
    #         resample = Image.BOX
    #     elif resample not in (
    #         Image.NEAREST,
    #         Image.BILINEAR,
    #         Image.BICUBIC,
    #         Image.LANCZOS,
    #         Image.BOX,
    #         Image.HAMMING,
    #     ):
    #         raise ValueError
    #     self._width *= mag
    #     self._height *= mag
    #     self._image = self._image.resize(
    #         (self._width, self._height), resample=resample  # type: ignore
    #     )
    #     return self._image

    # def __add__(self, other):
    #     """+演算子。画像を重ね合わせる。
    #     Args:
    #         other(NoiseImage): 重ね合わせる画像。
    #     Returns:
    #         重ね合わせた後の画像。
    #     Raises:
    #         TypeError: 重ね合わせる画像の型が合わない。
    #         ValueError: 重ね合わせる画像のサイズが合わない。
    #     """
    #     if type(other) != NoiseImage:
    #         raise TypeError
    #     if self._image.size != other.image.size:
    #         raise ValueError
    #     return Image.blend(self._image, other.image, 0.5)

    # def __iadd_(self, other):
    #     """+=演算子。画像を重ね合わせる。
    #     Args:
    #         other(NoiseImage): 重ね合わせる画像。
    #     Returns:
    #         重ね合わせた後の画像。
    #     Raises:
    #         TypeError: 重ね合わせる画像の型が合わない。
    #         ValueError: 重ね合わせる画像のサイズが合わない。
    #     """
    #     self = self + other
    #     return self
