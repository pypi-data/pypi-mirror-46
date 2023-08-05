import numpy as np
import miepy
import matplotlib.pyplot as plt
from my_pytools.my_matplotlib.colors import cmap

nm = 1e-9
wav = 600*nm
k = 2*np.pi*1.33/wav
medium = miepy.materials.water()

source = miepy.sources.gaussian_beam(width=300*nm, polarization=[1,0])
source = miepy.sources.radial_beam(width=400*nm)
interface = miepy.interface(miepy.constant_material(index=1.5))

reflected = interface.reflected_beam(source, wav, medium)

theta = np.linspace(0, np.pi/2, 200)
theta_r = np.linspace(np.pi, np.pi/2, 200)
r_par, r_perp = interface.reflection_coefficients(theta, wav, medium)

fig, ax = plt.subplots()
ax.plot(theta*180/np.pi, np.abs(r_par.real), label='r (parallel)', color='k')
ax.plot(theta*180/np.pi, np.abs(r_perp.real), label='r (perpendicular)', color='k', ls='--')

E = source.angular_spectrum(theta, 0, k)
I = np.sum(np.abs(E)**2, axis=0)
Imax = np.max(I)
I /= Imax
ax.plot(theta*180/np.pi, I**.5, label='incident beam')

E = reflected.angular_spectrum(theta, 0, k)
I = np.sum(np.abs(E)**2, axis=0)
I /= np.max(I)
ax.plot(180*theta/np.pi, I**.5, label='reflected beam')

ax.set(xlabel='angle of incidence (degrees)', ylabel='amplitude')
ax.margins(x=0)
ax.set_ylim(bottom=0)

ax.legend()

plt.savefig('a1.pdf')

fig, axes = plt.subplots(ncols=3, figsize=(12,5))
ax = axes[0]
scope = miepy.microscope(lambda theta, phi: reflected.angular_spectrum(theta, phi, k), 1.33, wav)

M = scope.magnification
xmax = 900*nm
x = np.linspace(-xmax, xmax)
image = scope.image(x*M, x*M)
I = np.sum(np.abs(image)**2, axis=0)

im = ax.pcolormesh(x/nm, x/nm, I.T/1e6, cmap='gray', rasterized=True)
ax.set_aspect('equal')
# plt.colorbar(im, ax=ax)
ax.set_title('water-glass', weight='bold')

ax = axes[1]
interface = miepy.interface(miepy.materials.metal())
reflected = interface.reflected_beam(source, wav, medium)

scope = miepy.microscope(lambda theta, phi: reflected.angular_spectrum(theta, phi, k), 1.33, wav)

image = scope.image(x*M, x*M)
I = np.sum(np.abs(image)**2, axis=0)

im = ax.pcolormesh(x/nm, x/nm, I.T/1e6, cmap='gray', rasterized=True)
ax.set_aspect('equal')
ax.set_title('water-mirror', weight='bold')
# plt.colorbar(im, ax=ax)


ax = axes[2]
x = np.linspace(-xmax, xmax, 50)
y = np.linspace(-xmax, xmax, 50)
X,Y = np.meshgrid(x, y)
Z = np.zeros_like(X)
E = source.E_field(X, Y, Z, k)
I = np.sum(np.abs(E)**2, axis=0)

ax.pcolormesh(X/nm, Y/nm, I, cmap=cmap['parula'], rasterized=True)
ax.set_aspect('equal')
ax.set_title('near field intensity', weight='bold')

for ax in axes:
    ax.set_xlabel('x (nm)')
axes[0].set_ylabel('y (nm)')

plt.savefig('a2.pdf')

fig, ax = plt.subplots()
x = np.linspace(-xmax, xmax, 200)
E = source.E_field(x, np.zeros_like(x), np.zeros_like(x), k)
I = np.sum(np.abs(E)**2, axis=0)
ax.plot(x/nm, I/np.max(I), label='near field')

interface = miepy.interface(miepy.constant_material(index=1.5))
reflected = interface.reflected_beam(source, wav, medium)
scope = miepy.microscope(lambda theta, phi: reflected.angular_spectrum(theta, phi, k), 1.33, wav)

M = scope.magnification
image = scope.image(x*M, [0])
I = np.sum(np.abs(image)**2, axis=0)
ax.plot(x/nm, I/np.max(I), label='image')
ax.margins(x=0)
ax.set_ylim(bottom=0)
ax.legend()
ax.set(xlabel='x (nm)',ylabel='intensity')
plt.savefig('a3.pdf')


plt.show()
