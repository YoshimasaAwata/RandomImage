from enum import Enum
import numpy as np
from PIL import Image
from abc import ABCMeta, abstractmethod


class ColorType(Enum):
    """2D画像をカラーで作成するかグレースケールで作成するかの指定を行う列挙型。"""

    GRAYSCALE = 1  # グレー
    RGB = 3  # RGBカラー


class NoiseImage(metaclass=ABCMeta):
    """乱数を使用した2Dのノイズ画像を生成する抽象クラス。"""

    def __init__(
        self,
        width: int = 512,
        height: int = 512,
        color: ColorType | str = ColorType.RGB,
        seed: int = -1,
    ) -> None:
        """カラーもしくはグレーで2Dのノイズ画像を生成するためのパラメーターを初期化。

        Args:
            width(int): 画像の幅。16ピクセル以上で16の倍数。
            height(int): 画像の高さ。16ピクセル以上で16の倍数。
            color(ColorType | str): カラーかグレーかの指定。
            seed(int): 乱数発生のシード値。0もしくは負数は自動設定。

        Raises:
            ValueError: 画像サイズが条件に合わない場合。
        """
        if (width < 16) or (height < 16) or (width % 16 != 0) or (height % 16 != 0):
            raise ValueError("画像サイズは16x16以上で16の倍数として下さい。")
        self.width = width
        self.height = height
        self.color = color
        self.seed = seed
        self.__image: Image.Image | None = None

    @property
    def image(self) -> Image.Image | None:
        return self.__image

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def color(self) -> ColorType:
        return self.__color

    @property
    def seed(self) -> int:
        return self.__seed

    @width.setter
    def width(self, value: int):
        if (value < 16) or (value % 16 != 0):
            raise ValueError("画像の幅は16以上で16の倍数として下さい。")
        self.__width = value

    @height.setter
    def height(self, value: int):
        if (value < 16) or (value % 16 != 0):
            raise ValueError("画像の高さは16以上で16の倍数として下さい。")
        self.__height = value

    @color.setter
    def color(self, value: ColorType | str):
        if type(value) is ColorType:
            self.__color = value
        else:
            self.__color = NoiseImage.get_color_type(str(value))

    @seed.setter
    def seed(self, value: int):
        if value > 0:
            self.__seed = value
        else:
            np.random.seed()
            self.__seed = np.random.randint(1, np.iinfo(np.int32).max)
        np.random.seed(self.__seed)

    @image.setter
    def image(self, value: Image.Image | None):
        self.__image = value

    def _check_resample(self, resample: int) -> bool:
        """画像拡大時の拡大方法のチェック。

        Args:
            resample(int): 画像拡大時の拡大方法。

        Returns:
            bool: Image内に指定された拡大方法の場合True、それ以外はFalseが返る。
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

    @abstractmethod
    def create_image(self) -> Image.Image:
        """ノイズ画像生成の抽象メソッド。

        Returns:
            Image.Image: ノイズ画像。
        """
        pass

    def get_mono(self) -> Image.Image:
        """グレー画像の取得。

        Color.RGBが指定されている画像でもグレー画像を取得。
        画像が作成されていない場合には新たに画像が作成される。

        Returns:
            Image.Image: グレー画像。
        """
        image = (
            self.create_image().convert(mode="L")
            if self.image == None
            else self.image.convert(mode="L")
        )
        return image

    def get_reduced_color(self, low: int = 0, high: int = 255) -> Image.Image:
        """色の範囲を狭めた画像の取得。

        Args:
            low(int): 色の下限値。0～255。
            high(int): 色の上限値。0～255。

        Returns:
            Image.Image: 色の範囲を狭めた画像。

        Raises:
            ValueError: 色の指定が範囲外です。
        """

        if (low < 0) or (high > 255) or (low >= high):
            raise ValueError("色の範囲は0～255の間でlow < highになるように指定して下さい。")
        image = self.create_image() if self.image == None else self.image
        rimage = np.array(image).astype(np.uint32)
        rimage *= high - low
        rimage //= 255
        rimage += low
        final_image = Image.fromarray(rimage.astype(np.uint8))
        return final_image

    def __add__(self, other):
        """+演算子。画像を重ね合わせる。
        Args:
            other(NoiseImage): 重ね合わせる画像。
        Returns:
            重ね合わせた後の画像。
        Raises:
            TypeError: 重ね合わせる画像の型が合わない。
            ValueError: 重ね合わせる画像のサイズが合わない。
        """
        if (type(other) != NoiseImage) or (other.image == None) or (self.image == None):
            raise TypeError
        elif self.image.size != other.image.size:
            raise ValueError
        return Image.blend(self.image, other.image, 0.5)

    def __iadd__(self, other):
        """+=演算子。画像を重ね合わせる。
        Args:
            other(NoiseImage): 重ね合わせる画像。
        Returns:
            重ね合わせた後の画像。
        Raises:
            TypeError: 重ね合わせる画像の型が合わない。
            ValueError: 重ね合わせる画像のサイズが合わない。
        """
        self = self + other
        return self

    @staticmethod
    def get_color_type(color: str) -> ColorType:
        """文字列から色のタイプを取得。

        RGBやグレースケールを示す文字列から列挙子に変える。
        指定する文字列に問題がある場合には"RGB"を示す列挙子を返す。

        Args:
            color(str): "RGB"もしくは"GRAYSCALE"を文字列として指定。

        Returns:
            ColorType: "RGB"もしくは"GRAYSCALE"を示す列挙子。
        """
        if color.upper() == "GRAYSCALE":
            return ColorType.GRAYSCALE
        return ColorType.RGB

    @staticmethod
    def get_resample_type(resample: str) -> int:
        """補間方法を文字列からImageクラスのタイプに変換。

        Imageクラスに無い文字列を指定した場合にはImage.Noneを返す。

        Args:
            resample(str): 補間方法を指定する文字列。

        Returns:
            int: Imageクラスの補間タイプ。
        """
        if resample == "NEAREST":
            return Image.NEAREST
        elif resample == "BILINEAR":
            return Image.BILINEAR
        elif resample == "BICUBIC":
            return Image.BICUBIC
        elif resample == "LANCZOS":
            return Image.LANCZOS
        elif resample == "BOX":
            return Image.BOX
        elif resample == "HAMMING":
            return Image.HAMMING
        else:
            return Image.NONE
