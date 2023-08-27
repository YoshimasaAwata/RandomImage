from noise_image import Color, NoiseImage
from PIL import Image

class TurbulenceImage:
    '''山岳や雲のような2D画像をノイズ画像の重ね合わせで作成'''

    def __init__(self, width=512, height=512, number=5, resample=Image.NONE, color=Color.MONO, seed=-1) -> None:
        """カラーもしくはモノクロで2Dのノイズ画像を生成するためのパラメーターを初期化。
        Args:
            width(int): 画像の幅。16ピクセル以上。
            height(int): 画像の高さ。16ピクセル以上。
            number(int): 画像の重ね合わせの枚数。2～
            resumple: 画像拡大方法。Imageクラスの拡大方法を指定。
            color(Color): カラーかモノクロかの指定。
            seed(int): 乱数発生のシード値。0もしくは負数は自動設定。
        Raises:
            ValueError: 拡大方法の指定が誤り。
        """
        if resample is Image.NONE:
            resample = Image.BICUBIC
        elif resample not in (
            Image.NEAREST,
            Image.BILINEAR,
            Image.BICUBIC,
            Image.LANCZOS,
            Image.BOX,
            Image.HAMMING,
        ):
            raise ValueError
