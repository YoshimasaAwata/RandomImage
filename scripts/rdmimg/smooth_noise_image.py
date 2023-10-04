from PIL import Image
from rdmimg.noise_image import NoiseImage, ColorType
import numpy as np


class SmoothNoiseImage(NoiseImage):
    """乱数を使用した2Dのタイル状のノイズ画像を生成するクラス。"""

    def __init__(
        self,
        width: int = 512,
        height: int = 512,
        color: ColorType = ColorType.RGB,
        seed: int = -1,
        tile_size: int = 4,
        resample: Image.Resampling = Image.Resampling.BOX,
    ) -> None:
        """カラーもしくはグレーで2Dのノイズ画像を生成するためのパラメーターを初期化。

        Args:
            width(int): 画像の幅。16ピクセル以上。
            height(int): 画像の高さ。16ピクセル以上。
            color(ColorType): カラーかグレーかの指定。
            seed(int): 乱数発生のシード値。0もしくは負数は自動設定。
            tile_size(int): タイルのサイズ。正方形の1辺のピクセル数。
            resample(Image.Resampling): 拡大方法。Image.Resamplingクラスの拡大方法を指定。

        Raises:
            ValueError:
                画像サイズが条件に合わない場合。
                タイルサイズが0もしくは負数の場合か、拡大方法の指定が誤り。
        """
        super().__init__(width, height, color, seed)
        self.tile_size = tile_size
        self.resample = resample

    @property
    def tile_size(self) -> int:
        return self.__tile_size

    @property
    def resample(self) -> Image.Resampling:
        return self.__resample

    @tile_size.setter
    def tile_size(self, value: int):
        if (value <= 0) or (self.width % value != 0) or (self.height % value != 0):
            raise ValueError("タイルのサイズの指定が間違っています。")
        self.__tile_size = value

    @resample.setter
    def resample(self, value: Image.Resampling):
        if not self._check_resample(value):
            raise ValueError("拡大方法はImageに規定された値を用います。")
        self.__resample = value

    def create_image(self) -> Image.Image:
        """2Dのタイル状のノイズ画像を生成。

        Returns:
            Image.Image: 2Dのタイル状のノイズ画像。
        """
        width = self.width // self.tile_size
        height = self.height // self.tile_size
        image = NoiseImage.create_base_image(width, height, self.color)
        image = image.resize((self.width, self.height), resample=self.resample)
        self.image = image
        return image
