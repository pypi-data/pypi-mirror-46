import miepy
import numpy as np
import matplotlib.pyplot as plt

nm = 1e-9
wav = 600*nm
k = 2*np.pi/wav
width = 100*nm

source = miepy.sources.gaussian_beam(width, [1,0])
z = np.linspace(-6*wav, 6*wav, 1000)
E = source.E_field(np.zeros_like(z), np.zeros_like(z), z, k)

phase = np.unwrap(np.angle(E[0]))
guoy = phase - k*z
guoy -= np.average(guoy)

plt.plot(z/nm, phase)
plt.show()
