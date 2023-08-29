from matplotlib import pyplot as plt
from smooth_noise_image import SmoothNoiseImage, Color

plt.ion()

width = 768
height = 512
block_size = 4
noise_img = SmoothNoiseImage(width, height, color=Color.MONO)
plt.imshow(noise_img.create_image(), cmap="gray")  # type: ignore

print("done")
