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
        tile_size=4,
        resample=Image.NONE,
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
        if (tile_size <= 0) or (width % tile_size != 0) or (height % tile_size):
            raise ValueError("タイルのサイズの指定が間違っています。")
        super().__init__(width // tile_size, height // tile_size, color, seed)
        self.enlarge(tile_size, resample)
