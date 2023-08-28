from PIL import Image
from noise_image import NoiseImage, Color


class SmoothNoiseImage(NoiseImage):
    """乱数を使用した2Dのタイル状のノイズ画像を生成するクラス"""

    def __init__(
        self,
        width=512,
        height=512,
        color=Color.RGB,
        seed=-1,
        mag=1,
        resample=Image.NONE,
    ) -> None:
        """カラーもしくはモノクロで2Dのノイズ画像を生成するためのパラメーターを初期化。
        Args:
            width(int): 画像の幅。16ピクセル以上。
            height(int): 画像の高さ。16ピクセル以上。
            color(Color): カラーかモノクロかの指定。
            seed(int): 乱数発生のシード値。0もしくは負数は自動設定。
            mag(int): 拡大率。
            resample: 拡大方法。Imageクラスの拡大方法を指定。
        Raises:
            ValueError: 画像サイズが条件に合わない場合。拡大率が0もしくは負数の場合か、拡大方法の指定が誤り。
        """
        super().__init__(width, height, color, seed)
        self.enlarge(mag, resample)
