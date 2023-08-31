from enum import Enum, auto
from noise_image import Color, NoiseImage
from PIL import Image


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
            background: 背景色。(r, g, b)を0-255で指定。

        Raises:
            ValueError:
                画像サイズが条件に合わない場合。重ね合わせる画像の数や拡大方法の指定が誤り。
                タイルの最大サイズや数に誤り。
                バックグラウンドカラーの指定に誤り。
        """
        super().__init__(width, height, color, seed)
        self.shape = shape
        self.max_tile_size = max_tile_size
        self.tile_num = tile_num
        self.background = background

    @property
    def shape(self) -> Shape:
        return self.__frag_shape

    @property
    def max_tile_size(self) -> int:
        return self.__max_tile_size

    @property
    def tile_num(self) -> int:
        return self.__tile_num

    @property
    def background(self) -> tuple:
        return self.__background

    @shape.setter
    def shape(self, value: Shape):
        self.__frag_shape = value

    @max_tile_size.setter
    def max_tile_size(self, value: int):
        if (value <= 0) or (value >= self.width) or (value >= self.height):
            raise ValueError("タイルの最大サイズは正数で画像サイズ未満です。")
        self.__max_tile_size = value

    @tile_num.setter
    def tile_num(self, value: int):
        if value <= 0:
            raise ValueError("タイルの数は正数です。")
        self.__tile_num = value

    @background.setter
    def background(self, value: tuple | list):
        if len(value) != 3:
            raise ValueError("バックグラウンドカラーは(r, g, b)の形式です。")
        for n in value:
            if (type(n) is not int) or (n < 0) or (n >= 256):
                raise ValueError("バックグラウンドカラーの要素は0～255の整数です。")
        self.__background = value if type(value) is tuple else tuple(value)

    def create_image(self) -> Image.Image:
        """タイルがランダムに配置された画像を生成、取得。

        Returns:
            Image.Image: ノイズ画像。
        """
        pass
