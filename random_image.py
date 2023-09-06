import gradio as gr
from noise_image import NoiseImage, ColorType
from smooth_noise_image import SmoothNoiseImage
from turbulence_image import TurbulenceImage

# 以下、コンポーネントの配置。
with gr.Blocks() as random_image:
    gr.Markdown("# ランダム画像を生成")
    iamge_generator = gr.State(SmoothNoiseImage())
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Tab(label="Smooth") as smooth_tab:
                tile_size = gr.Radio([2, 4, 8, 16], value=4, label="Tile size")
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
                shape = gr.Dropdown(
                    ["SQUARE", "RECTANGLE", "TRIANGLE", "CIRCLE", "ELLIPSIS"],
                    value="SQUARE",
                    label="Shape",
                )
                max_size = gr.Slider(
                    minimum=4, maximum=64, value=32, step=4, label="Max tile size"
                )
                tile_num = gr.Number(
                    value=10000, label="Tile num", precision=0, minimum=1
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
                label="Seed",
                precision=0,
                minimum=-1,
                maximum=2147483647,
                step=1,
            )
        with gr.Column(scale=2):
            output = gr.Image(type="pil", label="Output image", interactive=False)
            with gr.Row():
                create_btn = gr.Button(value="Create image")
                clear_btn = gr.Button(value="Clear")
                save_btn = gr.Button(value="Save")


# 以下、イベントハンドラーとイベント。
def select_smooth(
    width: int, height: int, color: str, seed: int, size: int, resample: str
) -> SmoothNoiseImage:
    """SmoothNoiseImageを選択。

    ノイズ画像を作成するインスタンスをSmoothNoiseImageに変更。

    Args:
        width(int): 画像の幅。
        height(int): 画像の高さ。
        color(str): "RGB"もしくは"GRAYSCALE"
        seed(int): -1以上の整数。
        size(int): タイルの1辺のサイズ。
        resample(str): 補間方法を表す文字列。

    Returns:
        SmoothNoiseImage: 新たに作成されたSmoothNoiseImageのインスタンス。
    """
    generator = SmoothNoiseImage(
        width,
        height,
        NoiseImage.get_color_type(color),
        seed,
        size,
        NoiseImage.get_resample_type(resample),
    )
    return generator


smooth_tab.select(
    select_smooth,
    inputs=[
        image_width,
        image_height,
        image_color,
        rand_seed,
        tile_size,
        resample_smooth,
    ],
    outputs=iamge_generator,
)


def change_image_size(
    generator: NoiseImage, width: int, hight: int
) -> tuple[NoiseImage, dict]:
    """ノイズ画像のサイズ変更。

    TurbulenceImageの重ね合わせ枚数の最大値を変更。
    また、スライダーの最大値を画像の幅と高さに合わせて変更する。

    Args:
        generator(NoiseImage): 画像作成のクラス。
        width(int): 画像の幅。
        height(int): 画像の高さ。

    Returns:
        NoiseImage: 画像作成のクラス。
        dict: アップデート後の重ね合わせ枚数を選択するスライダー。
    """
    num = TurbulenceImage.get_max_superposition(width, hight)
    generator.width = width
    generator.height = hight
    return generator, gr.Slider.update(maximum=int(num))


image_width.change(
    change_image_size,
    inputs=[iamge_generator, image_width, image_height],
    outputs=[iamge_generator, superposition],
)
image_height.change(
    change_image_size,
    inputs=[iamge_generator, image_width, image_height],
    outputs=[iamge_generator, superposition],
)

if __name__ == "__main__":
    random_image.launch()
