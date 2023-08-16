import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

plt.ion()

width = 768
height = 512
block_size = 4
rimage = np.random.randint(
    0, 256, (int(height / block_size), int(width / block_size), 3)
)
rimage = rimage.astype(np.uint8)
src_img = Image.fromarray(rimage)
dst_img = src_img.resize((width, height), resample=Image.BILINEAR)
plt.imshow(dst_img)  # type: ignore

print("done")
