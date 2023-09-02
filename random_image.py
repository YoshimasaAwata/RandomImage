from matplotlib import pyplot as plt
from smooth_noise_image import SmoothNoiseImage, Color
# from turbulence_image import TurbulenceImage
from tile_image import TileImage, Shape

plt.ion()

noise_img = TileImage(shape=Shape.TRIANGLE)
plt.imshow(noise_img.create_image())  # type: ignore

print("done")
