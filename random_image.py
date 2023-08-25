from matplotlib import pyplot as plt
from noise_image import *

plt.ion()

width = 768
height = 512
block_size = 4
noise_img = NoiseImage(int(width / block_size), int(height / block_size), block_size)
plt.imshow(noise_img.image)  # type: ignore

print("done")
