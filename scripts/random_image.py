from enum import Enum, auto
import gradio as gr
from PIL import Image

from rdmimg.noise_image import NoiseImage
from rdmimg.smooth_noise_image import SmoothNoiseImage
from rdmimg.tile_image import TileImage
from rdmimg.turbulence_image import TurbulenceImage


class ImageType(Enum):
    """ノイズ画像の種類。"""

    SMOOTH = auto()
    TURBULENCE = auto()
    TILE = auto()


# 以下、コンポーネントの配置。
with gr.Blocks(css="scripts/rdmimg/random_image.css") as random_image:
    gr.Markdown("# ランダム画像を生成")
    image_sta = gr.State(ImageType.SMOOTH)
    with gr.Row():
        with gr.Column():
            with gr.Tab(label="Smooth") as smooth_tab:
                tile_size_rdo = gr.Radio([2, 4, 8, 16, 32], value=4, label="Tile size")
                resample_smooth_drp = gr.Dropdown(
                    ["NEAREST", "BILINEAR", "BICUBIC", "LANCZOS", "BOX", "HAMMING"],
                    value="BOX",
                    label="Resample",
                )
            with gr.Tab(label="Turbulence") as turbulence_tab:
                superposition_sld = gr.Slider(
                    minimum=2,
                    maximum=6,
                    value=5,
                    step=1,
                    label="Superposition",
                    interactive=True,
                )
                resample_turbulence_drp = gr.Dropdown(
                    ["NEAREST", "BILINEAR", "BICUBIC", "LANCZOS", "BOX", "HAMMING"],
                    value="BICUBIC",
                    label="Resample",
                )
            with gr.Tab(label="Tile") as tile_tab:
                tile_shape_drp = gr.Dropdown(
                    ["SQUARE", "RECTANGLE", "TRIANGLE", "CIRCLE", "ELLIPSIS"],
                    value="SQUARE",
                    label="Shape",
                )
                max_tile_size_sld = gr.Slider(
                    minimum=4, maximum=64, value=32, step=4, label="Max tile size"
                )
                tile_num = gr.Number(
                    value=10000, label="Tile num (1～)", precision=0, minimum=1
                )
                background_pck = gr.ColorPicker(
                    value="#FFFFFF", label="Background", interactive=True
                )
            with gr.Row():
                with gr.Column(scale=8):
                    image_width_sld = gr.Slider(
                        minimum=128, maximum=8192, value=512, step=32, label="Width"
                    )
                    image_height_sld = gr.Slider(
                        minimum=128, maximum=8192, value=512, step=32, label="Height"
                    )
                exchange_btn = gr.Button(
                    value="⇧⇩",
                    scale=1,
                    size="sm",
                    min_width=32,
                    elem_id="ex_btn",
                )
            with gr.Row():
                size_512_btn = gr.Button(value="512x512", size="sm", min_width=64)
                size_768_btn = gr.Button(value="768x768", size="sm", min_width=64)
                size_1024_btn = gr.Button(value="1024x1024", size="sm", min_width=64)
                size_1152_btn = gr.Button(value="1152x896", size="sm", min_width=64)
                size_1344_btn = gr.Button(value="1344x768", size="sm", min_width=64)
            image_color_rdo = gr.Radio(["RGB", "GRAYSCALE"], value="RGB", label="Color")
            rand_seed_num = gr.Number(
                value=-1,
                label="Seed (-1 or 0～2147483647)",
                precision=0,
                minimum=-1,
                maximum=2147483647,
                step=1,
            )
        with gr.Column():
            output_img = gr.Image(
                type="pil",
                label="Output image",
                interactive=False,
                elem_id="img_box",
            )
            with gr.Row():
                create_btn = gr.Button(value="Create image")
                clear_btn = gr.Button(value="Clear", interactive=False)
            with gr.Row():
                used_seed_num = gr.Number(
                    label="Seed actually used", interactive=False, scale=2
                )

    # 以下、イベントハンドラーとイベント。
    smooth_tab.select(lambda: ImageType.SMOOTH, outputs=image_sta)
    turbulence_tab.select(lambda: ImageType.TURBULENCE, outputs=image_sta)
    tile_tab.select(lambda: ImageType.TILE, outputs=image_sta)

    def change_image_size(image_num: int, width: int, hight: int) -> dict:
        """ノイズ画像のサイズ変更。

        TurbulenceImageの重ね合わせ枚数の最大値を変更。
        また、スライダーの最大値を画像の幅と高さに合わせて変更する。

        Args:
            image_num(int): 画像の重ね合わせの枚数。
            width(int): 画像の幅。
            height(int): 画像の高さ。

        Returns:
            dict: アップデート後の重ね合わせ枚数を選択するスライダーの設定。
        """
        num = TurbulenceImage.get_max_superposition(width, hight)
        if num < image_num:
            return gr.Slider.update(maximum=int(num), value=int(num))
        else:
            return gr.Slider.update(maximum=int(num))

    image_width_sld.change(
        change_image_size,
        inputs=[superposition_sld, image_width_sld, image_height_sld],
        outputs=superposition_sld,
    )
    image_height_sld.change(
        change_image_size,
        inputs=[superposition_sld, image_width_sld, image_height_sld],
        outputs=superposition_sld,
    )

    exchange_btn.click(
        lambda width, height: (
            gr.Slider.update(value=height),
            gr.Slider.update(value=width),
        ),
        inputs=[image_width_sld, image_height_sld],
        outputs=[image_width_sld, image_height_sld],
    )

    size_512_btn.click(
        lambda: (
            gr.Slider.update(value=512),
            gr.Slider.update(value=512),
        ),
        outputs=[image_width_sld, image_height_sld],
    )

    size_768_btn.click(
        lambda: (
            gr.Slider.update(value=768),
            gr.Slider.update(value=768),
        ),
        outputs=[image_width_sld, image_height_sld],
    )

    size_1024_btn.click(
        lambda: (
            gr.Slider.update(value=1024),
            gr.Slider.update(value=1024),
        ),
        outputs=[image_width_sld, image_height_sld],
    )

    size_1152_btn.click(
        lambda: (
            gr.Slider.update(value=1152),
            gr.Slider.update(value=896),
        ),
        outputs=[image_width_sld, image_height_sld],
    )

    size_1344_btn.click(
        lambda: (
            gr.Slider.update(value=1344),
            gr.Slider.update(value=768),
        ),
        outputs=[image_width_sld, image_height_sld],
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
    ) -> tuple[int, Image.Image, dict]:
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
            dict: クリアボタンの設定。
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
        return creator.seed, creator.create_image(), gr.Button.update(interactive=True)

    create_btn.click(
        create_image,
        inputs=[
            image_sta,
            image_width_sld,
            image_height_sld,
            image_color_rdo,
            rand_seed_num,
            tile_size_rdo,
            resample_smooth_drp,
            superposition_sld,
            resample_turbulence_drp,
            tile_shape_drp,
            max_tile_size_sld,
            tile_num,
            background_pck,
        ],
        outputs=[used_seed_num, output_img, clear_btn],
    )

    clear_btn.click(
        lambda: (
            gr.Number.update(value=-1),
            gr.Image.update(value=None),
            gr.Button.update(interactive=False),
        ),
        outputs=[used_seed_num, output_img, clear_btn],
    )

if __name__ == "__main__":
    random_image.launch()
