from enum import Enum, auto
from noise_image import Color, NoiseImage


class Shape(Enum):
    """ランダムに配置するタイルの形状の指定を行う列挙型。"""

    SQUARE = auto()  # 正方形
    RECTANGLE = auto()  # 長方形
    TRIANGLE = auto()  # 三角形
    CIRCLE = auto()  # 円


class TileImage(NoiseImage):
    """タイルがランダムに配置された画像を生成するクラス"""

    def __init__(
        self,
        width=512,
        height=512,
        color=Color.RGB,
        seed=-1,
        shape=Shape.SQUARE,
        max_tile_size=32,
        tile_num=1000,
        background=(255, 255, 255),
    ) -> None:
        """カラーもしくはグレーでタイルがランダムに配置された2Dの画像を生成するためのパラメーターを初期化。
        Args:
            width(int): 画像の幅。16ピクセル以上。
            height(int): 画像の高さ。16ピクセル以上。
            color(Color): カラーかグレーかの指定。
            seed(int): 乱数発生のシード値。0もしくは負数は自動設定。
            shape(Shape): タイルの形状。
            max_tile_size(int): タイルの最大サイズ。
            tile_num(int): タイル数。
            backgrount: 背景色。(r, g, b)を0-255で指定。
        Raises:
            ValueError: 画像サイズが条件に合わない場合。重ね合わせる画像の数や拡大方法の指定が誤り。
        """
        super().__init__(width, height, color, seed)
