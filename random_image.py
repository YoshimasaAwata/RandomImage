from matplotlib import pyplot as plt
from smooth_noise_image import SmoothNoiseImage, Color
from turbulence_image import TurbulenceImage

plt.ion()

width = 512
height = 512
noise_img = TurbulenceImage(width, height, color=Color.RGB, number=6)
plt.imshow(noise_img.get_mono(), cmap="gray")  # type: ignore

print("done")
