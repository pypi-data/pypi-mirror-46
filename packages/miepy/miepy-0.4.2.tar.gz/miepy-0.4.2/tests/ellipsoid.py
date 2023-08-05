import miepy
import numpy as np
# import matplotlib.pyplot as plt

def main():
    nm = 1e-9

    rx = ry = 90*nm
    rz = 120*nm

    material = miepy.materials.Ag()
    wavelength = 700*nm
    lmax = 7


    e = miepy.spheroid([0,0,0], rx, rz, material, orientation=miepy.quaternion.from_spherical_coords(np.pi/2, 0))
    T1 = e.compute_tmatrix(lmax, wavelength, 1.0)
    idx = np.abs(T1) > 1e-4
    # print(T1[idx])
    e = miepy.ellipsoid([0,0,0], rz, rx, ry, material)
    T2 = e.compute_tmatrix(lmax, wavelength, 1.0)
    idx = np.abs(T2) > 1e-4
    # print(T2[idx])
    # print(T2[0,0,0])
    rmax = lmax*(lmax+2)

    np.save('T1.npy', T1)
    np.save('T2.npy', T2)

    # for i in range(2):
        # for j in range(2):
            # for r in range(rmax):
                # for rp in range(rmax):
                    # id1 = np.s_[i,r,j,rp]
                    # Tval = T1[id1]
                    # if np.abs(Tval) < 1e-4:
                        # continue

                    # id2 = np.unravel_index((np.argmin(np.abs(T2 - T1[id1]))), T2.shape)
                    # print(f'{id1} -> {id2}')

    for r1,n1,m1 in miepy.mode_indices(lmax):
        for r2,n2,m2 in miepy.mode_indices(lmax):
            id1 = np.s_[1,r1,0,r2]
            Tval = T1[id1]
            # if r1 != r2:
                # continue
            if np.abs(Tval) < 1e-6:
                continue

            id2 = np.unravel_index((np.argmin(np.abs(np.abs(T2) - np.abs(Tval)))), T2.shape)
            print(f'(n={n1}, m={m1}) -> (n={n2}, m={m2}) [{Tval:.3e}] -> {id2} [{T2[id2]:.3e}]')

def cross_section():
    nm = 1e-9

    rx = ry = 50*nm
    rz = 70*nm

    material = miepy.materials.Ag()
    wavelength = 700*nm
    lmax = 3
    source = miepy.sources.plane_wave([1,0])

    e = miepy.spheroid([0,0,0], rx, rz, material, orientation=miepy.quaternion.from_spherical_coords(np.pi/2, 0))
    c = miepy.cluster(particles=e,
                      source=source,
                      wavelength=wavelength,
                      lmax=lmax)
    print(c.cross_sections())

    e = miepy.ellipsoid([0,0,0], rz, ry, ry, material)
    c = miepy.cluster(particles=e,
                      source=source,
                      wavelength=wavelength,
                      lmax=lmax)
    print(c.cross_sections())

def compare_tmatrix():
    nm = 1e-9

    rx = ry = 60*nm
    rz = 1.3*rx

    material = miepy.materials.Ag()
    material = miepy.constant_material(4)
    wavelength = 600*nm
    lmax = 4


    e = miepy.spheroid([0,0,0], rx, rz, material, orientation=miepy.quaternion.from_spherical_coords(np.pi/2, np.pi/2))
    T1 = e.compute_tmatrix(lmax, wavelength, 1.0)
    e = miepy.ellipsoid([0,0,0], rx, rz, ry, material)
    T2 = e.compute_tmatrix(lmax, wavelength, 1.0)

    r = []
    for n in range(1, lmax+1):
        for m in range(-n, n+1):
            r.append((n,m))

    x = np.abs(T2 - T1).flatten()
    y = np.array(np.argsort(x)[-1000:])
    for yp in y:
        ind = np.unravel_index(yp, T2.shape)
        n1, m1 = r[ind[1]]
        n2, m2 = r[ind[3]]
        print(f'{(ind[0],) + r[ind[1]]} -> {(ind[2],) + r[ind[3]]}', T1[ind], T2[ind])

    # print(T1[1,:,0,0])
    # print(T2[1,:,0,0])
    # print(ind[-10:])

def post():
    lmax = 7
    rmax = lmax*(lmax+2)
    T1 = np.load('T1.npy')
    T2 = np.load('T2.npy')

    T2[0,:,1,:] = T2[1,::-1,0,:]
    T2[1,:,0,:] = T2[0,::-1,1,:]

    for r1,n1,m1 in miepy.mode_indices(lmax):
        for r2,n2,m2 in miepy.mode_indices(lmax):

            for i in range(2):
                for j in range(2):
                    if i == j:
                        continue
                    id1 = np.s_[i,r1,j,r2]
                    Tval = T1[id1]
                    if abs(Tval) < 1e-4:
                        continue

                    vals = np.argsort(np.abs(np.abs(T2) - np.abs(Tval)).flatten())[:10]
                    print(f'({i}, n={n1}, m={m1}) -> ({j}, n={n2}, m={m2}) [{Tval:.3e}]')
                    for val in vals:
                        id2 = np.unravel_index(val, T2.shape)
                        print(f'\t -> {id2} [{T2[id2]:.3e}]')
                    # id2 = np.unravel_index((np.argmin(np.abs(np.abs(T2) - np.abs(Tval)))), T2.shape)
                # if np.abs(Tval) < 1e-6:
                    # continue

            # print(f'(n={n1}, m={m1}) -> (n={n2}, m={m2}) [{Tval:.3e}] -> {id2} [{T2[id2]:.3e}]')

def test():
    for lmax in [4,5]:
        nm = 1e-9

        rx = ry = 40*nm
        rz = 60*nm

        material = miepy.materials.Ag()
        wavelength = 700*nm
        e = miepy.ellipsoid([0,0,0], rz, rx, ry, material)
        T = e.compute_tmatrix(lmax, wavelength, 1.0)

        T = T[1,:,0,:]
        val = -0.00018310308784968808+2.560697692166263e-07j
        idx = np.unravel_index(np.argmin(np.abs(T - val)), T.shape)
        print(idx, T[idx])



compare_tmatrix()
