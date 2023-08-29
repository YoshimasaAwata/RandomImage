from noise_image import Color, NoiseImage
from smooth_noise_image import SmoothNoiseImage
from PIL import Image


class TurbulenceImage(NoiseImage):
    """山岳や雲のような2D画像をノイズ画像の重ね合わせで作成"""

    def __init__(
        self,
        width=512,
        height=512,
        color=Color.MONO,
        seed=-1,
        number=5,
        resample=Image.NONE,
    ) -> None:
        """カラーもしくはモノクロで2Dのノイズ画像を生成するためのパラメーターを初期化。
        Args:
            width(int): 画像の幅。16ピクセル以上。
            height(int): 画像の高さ。16ピクセル以上。
            color(Color): カラーかモノクロかの指定。
            seed(int): 乱数発生のシード値。0もしくは負数は自動設定。
            number(int): 画像の重ね合わせの枚数。2～
            resumple: 画像拡大方法。Imageクラスの拡大方法を指定。
        Raises:
            ValueError: 画像サイズが条件に合わない場合。重ね合わせる画像の数や拡大方法の指定が誤り。
        """
        super().__init__(width, height, color, seed)
        self.number = number
        self.resample = resample
        # tile_size = 2 ** (number - 1)
        # if (number < 1) or (width // tile_size < 16) or (height // tile_size < 16):
        #     raise ValueError("重ね合わせる画像の数の指定に間違いがあります。")
        # # image = self.image.putalpha()
        # while tile_size > 1:
        #     new_width = width // tile_size
        #     new_height = height // tile_size
        #     noise_image = SmoothNoiseImage(
        #         new_width, new_height, self.__color, self.__seed, tile_size, resample
        #     )
        #     # images.append(noise_image.image)
        #     tile_size //= 2

    @property
    def number(self) -> int:
        return self.__number

    @property
    def resample(self) -> int:
        return self.__resample

    @number.setter
    def number(self, value: int):
        tile_size = 2 ** (value - 1)
        if (
            (value < 1)
            or (self.width // tile_size < 16)
            or (self.height // tile_size < 16)
        ):
            raise ValueError("重ね合わせる画像の数の指定に間違いがあります。")
        self.__number = value

    @resample.setter
    def resample(self, value: int):
        if not self._check_resample(value):
            raise ValueError("拡大方法はImageに規定された値を用います。")
        self.__resample = value
