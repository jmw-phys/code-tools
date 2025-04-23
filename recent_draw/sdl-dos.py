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
w_1, dos_1 = np.loadtxt("./norg-lno-dz.data", unpack=True,  usecols=(0, 2))
w_2, dos_2 = np.loadtxt("./ctqmc-lno-dz.data", unpack=True, usecols=(0, 2))
title = "1d-dos"

# ax.plot(w_1, dos_1, linestyle='-', alpha=0.8, clip_on=True, label=r"norg-$t_{2g}$")
ax.plot(w_1, dos_1, linestyle='-', alpha=0.8, clip_on=True, label="preblur0.02")
ax.plot(w_2, dos_2, linestyle='-', alpha=0.8, clip_on=True, label=r"ctqmc-$t_{2g}$")

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


