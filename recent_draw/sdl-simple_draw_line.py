#!/usr/local/bin/python3
##!/opt/homebrew/bin/python3
import sys
import numpy as np
import matplotlib
matplotlib.use("pdf") # setup backend
import matplotlib.pyplot as plt

matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'


#! e.g.: 5d_converge_test
# read data
w_1, dz_1, dx_1, dxz_1, dyz_1, dxy_1 = np.loadtxt("./sig.inp.22.1", unpack=True, usecols=(0, 2, 4, 6, 8, 10))
w_2, dz_2, dx_2, dxz_2, dyz_2, dxy_2 = np.loadtxt("./sig.inp.49.1", unpack=True, usecols=(0, 2, 4, 6, 8, 10))
# w_2, dz_2, dx_2, dxz_2, dyz_2, dxy_2 = np.loadtxt("./sig.inp.8.1", unpack=True, usecols=(0, 2, 4, 6, 8, 10))
# w_2, dz_2, dx_2, dxz_2, dyz_2, dxy_2 = np.loadtxt("./sig.inp.39.1", unpack=True, usecols=(0, 2, 4, 6, 8, 10))

# plot it
fig, ax = plt.subplots()
plt.subplots_adjust(hspace=0.0)

# title = "5d_58K-eg"
title = "5d_58K_VS_0K3bath-t2g"
# ax.plot(w_1, dz_1, linestyle='--', alpha=0.8, clip_on=True, label=r"58K-$d_{z^2}$")
# ax.plot(w_1, dx_1, linestyle='--', alpha=0.8, clip_on=True, label=r"58K-$d_{x^2-y^2}$")
ax.plot(w_1, dxz_1, linestyle='--', alpha=0.8, clip_on=True, label=r"58K-$d_{xz}$")
ax.plot(w_1, dyz_1, linestyle='--', alpha=0.8, clip_on=True, label=r"58K-$d_{yz}$")
ax.plot(w_1, dxy_1, linestyle='--', alpha=0.8, clip_on=True, label=r"58K-$d_{xy}$")
# ax.plot(w_2, dz_2, linestyle='-', alpha=0.8, clip_on=True, label=r"0K3bath-$d_{z^2}$")
# ax.plot(w_2, dx_2, linestyle='-', alpha=0.8, clip_on=True, label=r"0K3bath-$d_{x^2-y^2}$")
ax.plot(w_2, dxz_2, linestyle='-', alpha=0.8, clip_on=True, label=r"0K3bath-$d_{xz}$")
ax.plot(w_2, dyz_2, linestyle='-', alpha=0.8, clip_on=True, label=r"0K3bath-$d_{yz}$")
ax.plot(w_2, dxy_2, linestyle='-', alpha=0.8, clip_on=True, label=r"0K3bath-$d_{xy}$")

#  marker='o',
#  marker='o',
#  marker='o',
#  marker='o',
#  marker='o',
#  marker='x',
#  marker='x',
#  marker='x',
#  marker='x',
#  marker='x',



# setup labels
ax.set_ylabel(r'${\rm Im} G(i \omega)$')
ax.set_xlabel(r'$i \omega$ (eV)')
ax.legend()

# setup x and y range
ax.set_xlim(0, 3)
ax.set_ylim(-1.2, 0.0)

x_range = f"{ax.get_xlim()[0]}_{ax.get_xlim()[1]}"

# output the figure
plt.savefig(title+x_range+".pdf", bbox_inches='tight')
# plt.savefig(title+x_range+".png", bbox_inches='tight', dpi=300)





""" <!-- Kondo -->
import sys
import numpy as np
import matplotlib
matplotlib.use("pdf") # setup backend
import matplotlib.pyplot as plt

matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

# read data
w, A_s = np.loadtxt("./U3Re-hhdex3.out", unpack=True, usecols=(0, 4))
w, A_d = np.loadtxt("./U3Re-hhdex4.out", unpack=True, usecols=(0, 4))
w, A_sd = np.loadtxt("./U3Re-hhdex5.out", unpack=True, usecols=(0, 4))
w, gf = np.loadtxt("./U3Re-gfimp.out", unpack=True, usecols=(0, 4))

# plot it
fig, ax = plt.subplots()
plt.subplots_adjust(hspace=0.0)

mirrored_A_s = np.flip(A_s)
mirrored_A_d = np.flip(A_d)
mirrored_A_sd = np.flip(A_sd)
ax.plot(w, A_s + mirrored_A_s, linestyle='--', marker='o', alpha=0.8, clip_on=True, label=r"$A_{S}$")
ax.plot(w, A_d + mirrored_A_d, linestyle='--', marker='o', alpha=0.8, clip_on=True, label=r"$A_{D}$")
ax.plot(w, A_sd + mirrored_A_sd, linestyle='--', marker='o', alpha=0.8, clip_on=True, label=r"$A_{S+D}$")
ax.plot(w, gf, linestyle='-.', marker='x', alpha=0.8, clip_on=True, label=r"$Im(G)$")

# setup labels
ax.set_ylabel(r'$G(\omega)$')
ax.set_xlabel(r'$\omega$ (eV)')
ax.legend()

# setup x and y range
ax.set_xlim(-0.5, 0.5)
ax.set_ylim(-1.2, 0.0)

# output the figure
plt.savefig("Kondo_Unraveling.pdf", bbox_inches='tight')
plt.savefig("Kondo_Unraveling.png", bbox_inches='tight', dpi=300)




<!-- up down two subfigs -->
import sys
import numpy
import scipy.interpolate
import matplotlib
#matplotlib.use("Agg") # setup backend
matplotlib.use("pdf") # setup backend
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Polygon

matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

plt.figure(0)
############

# read data
w_norg_t2g, norg_t2g = numpy.loadtxt("./norg-dos/t2g/Aout.data", unpack = True, usecols = (0,1))
w_norg_eg, norg_eg = numpy.loadtxt("./norg-dos/eg/Aout.data", unpack = True, usecols = (0,1))
w_ctqmc_t2g, ctqmc_t2g = numpy.loadtxt("./ctqmc-dos/t2g/Aout.data", unpack = True, usecols = (0,1))
w_ctqmc_eg, ctqmc_eg = numpy.loadtxt("./ctqmc-dos/eg/Aout.data", unpack = True, usecols = (0,1))

# plot it
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
plt.subplots_adjust(hspace = 0.0)
lines1 = ax1.plot(w_norg_t2g, norg_t2g, alpha = 0.8, clip_on = True, label = r"V-3$d~$($t_{2g}$)")
lines2 = ax1.plot(w_norg_eg, norg_eg, alpha = 0.8, clip_on = True, label = r"V-3$d~$($e_{g}$)")
lines3 = ax2.plot(w_ctqmc_t2g, ctqmc_t2g, alpha = 0.8, clip_on = True, label = r"V-3$d~$($t_{2g}$)")
lines4 = ax2.plot(w_ctqmc_eg, ctqmc_eg, alpha = 0.8, clip_on = True, label = r"V-3$d~$($e_{g}$)")
ax1.fill_between(w_norg_t2g, norg_t2g, color = lines1[0].get_color(), alpha = 0.1)
ax1.fill_between(w_norg_eg, norg_eg, color = lines2[0].get_color(), alpha = 0.1)
ax2.fill_between(w_ctqmc_t2g, ctqmc_t2g, color = lines3[0].get_color(), alpha = 0.1)
ax2.fill_between(w_ctqmc_eg, ctqmc_eg, color = lines4[0].get_color(), alpha = 0.1)
ax1.axvline(0, linestyle = '--', color = 'purple')
ax2.axvline(0, linestyle = '--', color = 'purple')

# setup line properties

# setup tics
ax1.set_yticks([0, 0.4, 0.8, 1.2])
ax2.set_yticks([0, 0.4, 0.8])
ax1.tick_params(length = 4, width = 0.5, direction = 'in', top=True, right=True)
ax2.tick_params(length = 4, width = 0.5, direction = 'in', top=True, right=True)

# setup labels
ax2.set_ylabel(r'$A(\omega)$')
ax2.set_xlabel(r'$\omega$ (eV)')
ax1.set_ylabel(r'$A(\omega)$')
ax1.annotate('(a)', xy=(0.03, 0.88), xycoords='axes fraction')
ax2.annotate('(b)', xy=(0.03, 0.88), xycoords='axes fraction')
ax1.legend()
ax2.legend()

# setup x and y range
ax1.set_xlim(-4, 8)
ax2.set_xlim(-4, 8)
ax1.set_ylim(0, 1.2)
ax2.set_ylim(0, 1.2)

# output the figure
plt.savefig("svo-dos", bbox_inches='tight')
plt.savefig("svo-dos.png", bbox_inches='tight')
"""