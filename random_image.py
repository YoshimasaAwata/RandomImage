import math
import gradio as gr

from turbulence_image import TurbulenceImage

with gr.Blocks() as demo:
    gr.Markdown(
    """
    # Hello World!
    Start typing below to see the output.
    """)
    with gr.Row():
        output = gr.Image()
        with gr.Column():
            with gr.Tab(label="Smooth"):
                tile_size = gr.Radio([2, 4, 8, 16], value=4, label="Tile size")
                resample_s = gr.Dropdown(["NEAREST", "BILINEAR", "BICUBIC", "LANCZOS", "BOX", "HAMMING"], value="BOX", label="Resample")
            with gr.Tab(label="Turbulence"):
                superposition = gr.Slider(minimum=2, maximum=6, value=5, step=1, label="Superposition", interactive=True)
                resample_t = gr.Dropdown(["NEAREST", "BILINEAR", "BICUBIC", "LANCZOS", "BOX", "HAMMING"], value="BOX", label="Resample")
            with gr.Tab(label="Tile"):
                shape = gr.Dropdown(["SQUARE", "RECTANGLE", "TRIANGLE", "CIRCLE", "ELLIPSIS"], value="SQUARE", label="Shape")
                max_size = gr.Slider(minimum=4, maximum=64, value=32, step=4, label="Max tile size")
                tile_num = gr.Number(value=10000, label="Tile num", precision=0, minimum=1)
                # バックグラウンドカラー
            width = gr.Slider(minimum=128, maximum=8192, value=512, step=16, label="Width")
            height = gr.Slider(minimum=128, maximum=8192, value=512, step=16, label="Height")
            color = gr.Radio(["RGB", "GRAYSCALE"], value="RGB", label="Color")
            # seed

            def change_superposition(width, height):
                num = math.log2(width) if width < height else math.log2(height)
                num -= 3
                return gr.Slider.update(maximum=int(num))
            width.change(change_superposition, inputs=[width, height], outputs=superposition)
            height.change(change_superposition, inputs=[width, height], outputs=superposition)

if __name__ == "__main__":
    demo.launch()
