from PIL import Image
from noise_image import NoiseImage, Color
import numpy as np


class SmoothNoiseImage(NoiseImage):
    """乱数を使用した2Dのタイル状のノイズ画像を生成するクラス。"""

    def __init__(
        self,
        width=512,
        height=512,
        color=Color.RGB,
        seed=-1,
        tile_size=4,
        resample=Image.BOX,
    ) -> None:
        """カラーもしくはモノクロで2Dのノイズ画像を生成するためのパラメーターを初期化。
        Args:
            width(int): 画像の幅。16ピクセル以上。
            height(int): 画像の高さ。16ピクセル以上。
            color(Color): カラーかモノクロかの指定。
            seed(int): 乱数発生のシード値。0もしくは負数は自動設定。
            tile_size(int): タイルのサイズ。正方形の1辺のピクセル数。
            resample: 拡大方法。Imageクラスの拡大方法を指定。
        Raises:
            ValueError: 画像サイズが条件に合わない場合。タイルサイズが0もしくは負数の場合か、拡大方法の指定が誤り。
        """
        super().__init__(width // tile_size, height // tile_size, color, seed)
        self.tile_size = tile_size
        self.resample = resample

    @property
    def tile_size(self) -> int:
        return self.__tile_size

    @property
    def resample(self) -> int:
        return self.__resample

    @tile_size.setter
    def tile_size(self, value: int):
        if (value <= 0) or (self.width % value != 0) or (self.height % value != 0):
            raise ValueError("タイルのサイズの指定が間違っています。")
        self.__tile_size = value

    @resample.setter
    def resample(self, value: int):
        if not self._check_resample(value):
            raise ValueError("拡大方法はImageに規定された値を用います。")
        self.__resample = value

    def create_image(self) -> Image.Image:
        """2Dのタイル状のノイズ画像を生成。"""
        width = self.width // self.tile_size
        height = self.height // self.tile_size
        image = SmoothNoiseImage.create_base_image(width, height, self.color)
        image = image.resize(
            (self.width, self.height), resample=self.resample  # type: ignore
        )
        self.image = image
        return image

    @staticmethod
    def create_base_image(width: int, height: int, color: Color) -> Image.Image:
        """基本となる2Dノイズ画像の作成。
        Args:
            width(int): 画像の幅。1以上。
            height(int): 画像の高さ。1以上。
            color(int): Color.MONOかColor.RGBか。
        Returns:
            2Dノイズ画像。
        """
        rimage = (
            np.random.randint(0, 256, (height, width, 3))
            if color == Color.RGB
            else np.random.randint(0, 256, (height, width))
        )
        image = Image.fromarray(rimage.astype(np.uint8))
        return image
