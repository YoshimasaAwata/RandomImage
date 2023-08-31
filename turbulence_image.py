import numpy as np
from noise_image import Color, NoiseImage
from smooth_noise_image import SmoothNoiseImage
from PIL import Image


class TurbulenceImage(NoiseImage):
    """山岳や雲のような2D画像をノイズ画像の重ね合わせで作成"""

    def __init__(
        self,
        width=512,
        height=512,
        color=Color.GRAY,
        seed=-1,
        number=5,
        resample=Image.BICUBIC,
    ) -> None:
        """カラーもしくはグレーで2Dのノイズ画像を生成するためのパラメーターを初期化。

        Args:
            width(int): 画像の幅。16ピクセル以上。
            height(int): 画像の高さ。16ピクセル以上。
            color(Color): カラーかグレーかの指定。
            seed(int): 乱数発生のシード値。0もしくは負数は自動設定。
            number(int): 画像の重ね合わせの枚数。2～
            resumple: 画像拡大方法。Imageクラスの拡大方法を指定。

        Raises:
            ValueError:
                画像サイズが条件に合わない場合。
                重ね合わせる画像の数や拡大方法の指定が誤り。
        """
        super().__init__(width, height, color, seed)
        self.number = number
        self.resample = resample

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

    def create_image(self) -> Image.Image:
        """山岳や雲のような2Dのノイズ画像を生成、取得。

        Returns:
            Image.Image: ノイズ画像。
        """
        tile_size = 2 ** (self.number - 1)
        total = (
            np.zeros((self.height, self.width, 3), dtype=np.int32)
            if self.color == Color.RGB
            else np.zeros((self.height, self.width), dtype=np.int32)
        )
        while tile_size >= 1:
            width = self.width // tile_size
            height = self.height // tile_size
            image = SmoothNoiseImage.create_base_image(width, height, self.color)
            image = image.resize((self.width, self.height), resample=self.resample)  # type: ignore
            total += np.array(image)
            tile_size //= 2
        final_image = Image.fromarray((total / 5).astype(np.uint8))
        self.image = final_image
        return final_image

    @staticmethod
    def check_param(width: int, height: int, number: int) -> bool:
        """画像の幅と高さ、重ね合わせ枚数が妥当かどうかの確認。

        Returns:
            bool: 妥当(True)か妥当でない(False)か。
        """
        tile_size = 2 ** (number - 1)
        result = (
            (width >= 16)
            and (width % 16 == 0)
            and (height >= 16)
            and (height % 16 == 0)
            and (number >= 2)
            and (width // tile_size >= 16)
            and (height // tile_size >= 16)
        )
        return result
