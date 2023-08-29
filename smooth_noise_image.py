from PIL import Image
from noise_image import NoiseImage, Color
import numpy as np


class SmoothNoiseImage(NoiseImage):
    """乱数を使用した2Dのタイル状のノイズ画像を生成するクラス"""

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
        if (tile_size <= 0) or (width % tile_size != 0) or (height % tile_size != 0):
            raise ValueError("タイルのサイズの指定が間違っています。")
        if not self._check_resample(resample):
            raise ValueError("拡大方法はImageに規定された値を用います。")
        super().__init__(width // tile_size, height // tile_size, color, seed)
        self.__tile_size = tile_size
        self.__resample = resample
        # self.enlarge(tile_size, resample)

    def _check_resample(self, resample) -> bool:
        """画像拡大時の拡大方法のチェック
        Args:
            resample(int): 画像拡大時の拡大方法。
        Returns:
            Image内に指定された拡大方法の場合True、それ以外はFalseが返る。
        """
        return resample in (
            Image.NONE,
            Image.NEAREST,
            Image.BILINEAR,
            Image.BICUBIC,
            Image.LANCZOS,
            Image.BOX,
            Image.HAMMING,
        )

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
        """2Dのタイル状のノイズ画像を生成"""
        orig_width = self.width // self.tile_size
        orig_height = self.height // self.tile_size
        rimage = (
            np.random.randint(0, 256, (orig_height, orig_width, 3))
            if self.color == Color.RGB
            else np.random.randint(0, 256, (orig_height, orig_width))
        )
        image = Image.fromarray(rimage.astype(np.uint8))
        image = image.resize(
            (self.width, self.height), resample=self.resample  # type: ignore
        )
        self.image = image
        return image
