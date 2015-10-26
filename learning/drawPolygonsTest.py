import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import matplotlib as mpl

import pdb

fig, ax = plt.subplots()
patches = []
N = 50

for i in range(N):
	polygon = Polygon(np.random.rand(N, 2), True)
	patches.append(polygon)

p = PatchCollection(patches, cmap=mpl.cm.jet, alpha=0.4)
colors = 255*np.random.rand(len(patches))
p.set_array(np.array(colors))
pdb.set_trace()
ax.add_collection(p)

plt.show()
