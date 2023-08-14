import numpy as np
from matplotlib import pyplot as plt

plt.ion()

rimage = np.random.randint(0, 256, (512, 512, 3))
plt.imshow(rimage)

print("done")
