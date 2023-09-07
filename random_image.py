from enum import Enum, auto
import gradio as gr
from PIL import Image
from noise_image import NoiseImage, ColorType
from smooth_noise_image import SmoothNoiseImage
from tile_image import TileImage
from turbulence_image import TurbulenceImage


class ImageType(Enum):
    """ノイズ画像の種類。"""

    SMOOTH = auto()
    TURBULENCE = auto()
    TILE = auto()


# 以下、コンポーネントの配置。
with gr.Blocks() as random_image:
    gr.Markdown("# ランダム画像を生成")
    image_type = gr.State(ImageType.SMOOTH)
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Tab(label="Smooth") as smooth_tab:
                tile_size = gr.Radio([2, 4, 8, 16, 32, 64], value=4, label="Tile size")
                resample_smooth = gr.Dropdown(
                    ["NEAREST", "BILINEAR", "BICUBIC", "LANCZOS", "BOX", "HAMMING"],
                    value="BOX",
                    label="Resample",
                )
            with gr.Tab(label="Turbulence") as turbulence_tab:
                superposition = gr.Slider(
                    minimum=2,
                    maximum=6,
                    value=5,
                    step=1,
                    label="Superposition",
                    interactive=True,
                )
                resample_turbulence = gr.Dropdown(
                    ["NEAREST", "BILINEAR", "BICUBIC", "LANCZOS", "BOX", "HAMMING"],
                    value="BICUBIC",
                    label="Resample",
                )
            with gr.Tab(label="Tile") as tile_tab:
                tile_shape = gr.Dropdown(
                    ["SQUARE", "RECTANGLE", "TRIANGLE", "CIRCLE", "ELLIPSIS"],
                    value="SQUARE",
                    label="Shape",
                )
                max_tile_size = gr.Slider(
                    minimum=4, maximum=64, value=32, step=4, label="Max tile size"
                )
                tile_num = gr.Number(
                    value=10000, label="Tile num (1～)", precision=0, minimum=1
                )
                background = gr.ColorPicker(
                    value="#FFFFFF", label="Background", interactive=True
                )
            image_width = gr.Slider(
                minimum=128, maximum=8192, value=512, step=16, label="Width"
            )
            image_height = gr.Slider(
                minimum=128, maximum=8192, value=512, step=16, label="Height"
            )
            image_color = gr.Radio(["RGB", "GRAYSCALE"], value="RGB", label="Color")
            rand_seed = gr.Number(
                value=-1,
                label="Seed (-1 or 0～2147483647)",
                precision=0,
                minimum=-1,
                maximum=2147483647,
                step=1,
            )
        with gr.Column(scale=2):
            output_image = gr.Image(type="pil", label="Output image", interactive=False)
            with gr.Row():
                create_btn = gr.Button(value="Create image")
                clear_btn = gr.Button(value="Clear")
                save_btn = gr.Button(value="Save")
            used_seed = gr.Number(label="Seed actually used", interactive=False)

    # 以下、イベントハンドラーとイベント。
    smooth_tab.select(lambda: ImageType.SMOOTH, outputs=image_type)
    turbulence_tab.select(lambda: ImageType.TURBULENCE, outputs=image_type)
    tile_tab.select(lambda: ImageType.TILE, outputs=image_type)

    def change_image_size(image_num: int, width: int, hight: int) -> dict:
        """ノイズ画像のサイズ変更。

        TurbulenceImageの重ね合わせ枚数の最大値を変更。
        また、スライダーの最大値を画像の幅と高さに合わせて変更する。

        Args:
            image_num(int): 画像の重ね合わせの枚数。
            width(int): 画像の幅。
            height(int): 画像の高さ。

        Returns:
            dict: アップデート後の重ね合わせ枚数を選択するスライダー。
        """
        num = TurbulenceImage.get_max_superposition(width, hight)
        if num < image_num:
            return gr.Slider.update(maximum=int(num), value=int(num))
        else:
            return gr.Slider.update(maximum=int(num))

    image_width.change(
        change_image_size,
        inputs=[superposition, image_width, image_height],
        outputs=superposition,
    )
    image_height.change(
        change_image_size,
        inputs=[superposition, image_width, image_height],
        outputs=superposition,
    )

    def create_image(
        type: ImageType,
        width: int,
        height: int,
        color: str,
        seed: int,
        t_size: int,
        resample_s: str,
        image_num: int,
        resample_t: str,
        shape: str,
        max_size: int,
        num: int,
        b_color: str,
    ) -> tuple[int, Image.Image]:
        """ノイズ画像を実際に作成。

        Args:
            type(ImageType): ノイズ画像の種類。
            width(int): 画像の幅。
            height(int): 画像の高さ。
            color(str): カラー("RGB")かグレースケール("GRAYSCALE")か。
            seed(int): 使用する乱数のseed。
            t_size(int): SmoothNoiseImageのタイルのサイズ。
            resample_s(str): SmoothNoiseImageの補間の種類。
            image_num(int): TurbulenceImageの画像の重ね合わせの枚数。
            resample_t(str): TurbulenceImageの補間の種類。
            shape(str): TileImageのタイルの形状。
            max_size(int): TileImageのタイルの最大サイズ。
            num(int): TileImageのタイルの枚数。
            b_color(str): TileImageのバックグラウンドカラー。

        Returns:
            int: 実際に使用したseed値。
            Image.Image: ノイズ画像。
        """
        color_type = NoiseImage.get_color_type(color)
        if type == ImageType.TILE:
            shape_type = TileImage.get_shape_type(shape)
            creator = TileImage(
                width, height, color_type, seed, shape_type, max_size, num, b_color
            )
        elif type == ImageType.TURBULENCE:
            resample = NoiseImage.get_resample_type(resample_t)
            creator = TurbulenceImage(
                width, height, color_type, seed, image_num, resample
            )
        else:  # type == ImageType.SMOOTH
            resample = NoiseImage.get_resample_type(resample_s)
            creator = SmoothNoiseImage(
                width, height, color_type, seed, t_size, resample
            )
        return creator.seed, creator.create_image()

    create_btn.click(
        create_image,
        inputs=[
            image_type,
            image_width,
            image_height,
            image_color,
            rand_seed,
            tile_size,
            resample_smooth,
            superposition,
            resample_turbulence,
            tile_shape,
            max_tile_size,
            tile_num,
            background,
        ],
        outputs=[used_seed, output_image],
    )

if __name__ == "__main__":
    random_image.launch()
