import matplotlib.pyplot as plt  # graph output
import numpy as np  # array math

x = np.arange(0., 3.*np.pi, 0.01)

plt.plot(x, np.cos(x**2.), 'b-', x, np.cos(x)**2., 'r-')
