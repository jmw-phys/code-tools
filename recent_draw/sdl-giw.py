#!/usr/local/bin/python3
# code developed and maintained by (jmw@ruc.edu.cn, RUC, China) date 2025
##!/opt/homebrew/bin/python3
import sys
import numpy as np
import matplotlib
matplotlib.use("pdf") # setup backend
import matplotlib.pyplot as plt


matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'


# plot it
fig, ax = plt.subplots()
plt.subplots_adjust(hspace=0.0)

# read data
w_1, t2g_1 = np.loadtxt("./norg-lno-dz.data", unpack=True,  usecols=(0, 2))
w_2, t2g_2 = np.loadtxt("./ctqmc-lno-dz.data", unpack=True, usecols=(0, 2))

title = "lno-dz"
ax.plot(w_1, t2g_1, linestyle='-', alpha=0.8, clip_on=True, label=r"norg-$t_{2g}$")
ax.plot(w_2, t2g_2, linestyle='-', alpha=0.8, clip_on=True, label=r"ctqmc-$t_{2g}$")

#  marker='o',
#  marker='x',

# setup labels
ax.set_ylabel(r'${\rm Im} G(i \omega)$')
ax.set_xlabel(r'$ \omega$ (eV)')
ax.legend()

# setup x and y range
ax.set_xlim(0, 3)
ax.set_ylim(-1.4, 0.0)
x_range = f"{ax.get_xlim()[0]}_{ax.get_xlim()[1]}"

# output the figure
plt.savefig(title+x_range+".pdf", bbox_inches='tight')
# plt.savefig(title+x_range+".png", bbox_inches='tight', dpi=300)


# plot it
fig, ax = plt.subplots()
plt.subplots_adjust(hspace=0.0)
w_1, eg_1 = np.loadtxt("./norg-lno-dx.data", unpack=True,  usecols=(0, 2))
w_2, eg_2 = np.loadtxt("./ctqmc-lno-dx.data", unpack=True, usecols=(0, 2))

title = "lno-dx"
ax.plot(w_1, eg_1, linestyle='-', alpha=0.8, clip_on=True, label=r"norg-$e_{g}$")
ax.plot(w_2, eg_2, linestyle='-', alpha=0.8, clip_on=True, label=r"ctqmc-$e_{g}$")

# setup labels
ax.set_ylabel(r'${\rm Im} G(i \omega)$')
ax.set_xlabel(r'$ \omega$ (eV)')
ax.legend()

# output the figure
plt.savefig(title+x_range+".pdf", bbox_inches='tight')