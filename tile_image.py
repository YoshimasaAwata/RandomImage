import numpy as np
from enum import Enum, auto
from noise_image import ColorType, NoiseImage
from PIL import Image, ImageDraw, ImageColor


class Shape(Enum):
    """ランダムに配置するタイルの形状の指定を行う列挙型。"""

    SQUARE = auto()  # 正方形
    RECTANGLE = auto()  # 長方形
    TRIANGLE = auto()  # 三角形
    CIRCLE = auto()  # 円
    ELLIPSIS = auto()  # 楕円


class TileImage(NoiseImage):
    """タイルがランダムに配置された画像を生成するクラス"""

    def __init__(
        self,
        width: int = 512,
        height: int = 512,
        color: ColorType = ColorType.RGB,
        seed: int = -1,
        shape: Shape = Shape.SQUARE,
        max_tile_size: int = 32,
        tile_num: int = 10000,
        background: str | tuple | list = (255, 255, 255),
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
            background(str | tuple | list): 背景色。文字列もしくは(r, g, b)を0-255で指定。

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
    def background(self, value: str | tuple | list):
        if type(value) is str:
            self._background = ImageColor.getrgb(value)
        else:
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

        mode = "RGB" if self.color == ColorType.RGB else "L"
        image = Image.new(mode, (self.width, self.height), self.background)
        brush = ImageDraw.Draw(image)
        draw_func = (
            self._draw_square
            if self.shape == Shape.SQUARE
            else self._draw_rectangle
            if self.shape == Shape.RECTANGLE
            else self._draw_triangle
            if self.shape == Shape.TRIANGLE
            else self._draw_circle
            if self.shape == Shape.CIRCLE
            else self._draw_ellipse
        )
        for n in range(self.tile_num):
            draw_func(brush)
        return image

    def _draw_square(self, brush: ImageDraw.ImageDraw):
        """1つのランダムな正方形を描画。

        Args:
            brush(ImageDraw.ImageDraw): 描画用ブラシ。
        """

        square_size = np.random.randint(1, self.max_tile_size)
        x0 = np.random.randint(0, self.width - square_size)
        y0 = np.random.randint(0, self.height - square_size)
        x1 = x0 + square_size
        y1 = y0 + square_size
        fg_color = tuple(np.random.randint(0, 255, 3).tolist())
        brush.rectangle((x0, y0, x1, y1), fill=fg_color)

    def _draw_rectangle(self, brush: ImageDraw.ImageDraw):
        """1つのランダムな長方形を描画。

        Args:
            brush(ImageDraw.ImageDraw): 描画用ブラシ。
        """

        rect_width = np.random.randint(1, self.max_tile_size)
        rect_height = np.random.randint(1, self.max_tile_size)
        x0 = np.random.randint(0, self.width - rect_width)
        y0 = np.random.randint(0, self.height - rect_height)
        x1 = x0 + rect_width
        y1 = y0 + rect_height
        fg_color = tuple(np.random.randint(0, 255, 3).tolist())
        brush.rectangle((x0, y0, x1, y1), fill=fg_color)

    def _draw_triangle(self, brush: ImageDraw.ImageDraw):
        """1つのランダムな三角形を描画。

        Args:
            brush(ImageDraw.ImageDraw): 描画用ブラシ。
        """

        x0 = np.random.randint(0, self.width)
        y0 = np.random.randint(0, self.height)
        x1 = x0 + np.random.randint(-self.max_tile_size, self.max_tile_size)
        y1 = y0 + np.random.randint(-self.max_tile_size, self.max_tile_size)
        x2 = x0 + np.random.randint(-self.max_tile_size, self.max_tile_size)
        y2 = y0 + np.random.randint(-self.max_tile_size, self.max_tile_size)
        fg_color = tuple(np.random.randint(0, 255, 3).tolist())
        brush.polygon((x0, y0, x1, y1, x2, y2), fill=fg_color)

    def _draw_circle(self, brush: ImageDraw.ImageDraw):
        """1つのランダムな円形を描画。

        Args:
            brush(ImageDraw.ImageDraw): 描画用ブラシ。
        """

        circle_radius = np.random.randint(1, self.max_tile_size)
        x0 = np.random.randint(0, self.width - circle_radius)
        y0 = np.random.randint(0, self.height - circle_radius)
        x1 = x0 + circle_radius
        y1 = y0 + circle_radius
        fg_color = tuple(np.random.randint(0, 255, 3).tolist())
        brush.ellipse((x0, y0, x1, y1), fill=fg_color)

    def _draw_ellipse(self, brush: ImageDraw.ImageDraw):
        """1つのランダムな楕円形を描画。

        Args:
            brush(ImageDraw.ImageDraw): 描画用ブラシ。
        """

        circle_width = np.random.randint(1, self.max_tile_size)
        circle_height = np.random.randint(1, self.max_tile_size)
        x0 = np.random.randint(0, self.width - circle_width)
        y0 = np.random.randint(0, self.height - circle_height)
        x1 = x0 + circle_width
        y1 = y0 + circle_height
        fg_color = tuple(np.random.randint(0, 255, 3).tolist())
        brush.ellipse((x0, y0, x1, y1), fill=fg_color)
