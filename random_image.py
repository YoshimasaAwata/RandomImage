import math
import gradio as gr
from noise_image import NoiseImage
from smooth_noise_image import SmoothNoiseImage
from turbulence_image import TurbulenceImage

# 以下、コンポーネントの配置。
with gr.Blocks() as random_image:
    gr.Markdown("# ランダム画像を生成")
    image = gr.State(SmoothNoiseImage())
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Tab(label="Smooth"):
                tile_size = gr.Radio([2, 4, 8, 16], value=4, label="Tile size")
                resample_smooth = gr.Dropdown(
                    ["NEAREST", "BILINEAR", "BICUBIC", "LANCZOS", "BOX", "HAMMING"],
                    value="BOX",
                    label="Resample",
                )
            with gr.Tab(label="Turbulence"):
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
            with gr.Tab(label="Tile"):
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
            width = gr.Slider(
                minimum=128, maximum=8192, value=512, step=16, label="Width"
            )
            height = gr.Slider(
                minimum=128, maximum=8192, value=512, step=16, label="Height"
            )
            color = gr.Radio(["RGB", "GRAYSCALE"], value="RGB", label="Color")
            seed = gr.Number(
                value=-1,
                label="Seed",
                precision=0,
                minimum=-1,
                maximum=2147483647,
                step=1,
            )
        with gr.Column(scale=2):
            output = gr.Image(type="pil", label="Output image", interactive=False)
            create_btn = gr.Button(value="Create image", size="sm")


# 以下、イベントハンドラーとイベント。
def change_image_size(im: NoiseImage, w: int, h: int):
    """ノイズ画像のサイズ変更。

    TurbulenceImageの重ね合わせ枚数の最大値を変更。
    また、スライダーの最大値を画像の幅と高さに合わせて変更する。

    Args:
        im(NoiseImage): 画像作成のクラス。
        w(int): 画像の幅。
        h(int): 画像の高さ。

    Returns:
        画像作成のクラス。
        アップデート後の重ね合わせ枚数を選択するスライダー。
    """
    num = TurbulenceImage.get_max_superposition(w, h)
    im.width = w
    im.height = h
    return image, gr.Slider.update(maximum=int(num))


width.change(
    change_image_size, inputs=[image, width, height], outputs=[image, superposition]
)
height.change(
    change_image_size, inputs=[image, width, height], outputs=[image, superposition]
)

if __name__ == "__main__":
    random_image.launch()
