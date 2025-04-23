#!/usr/local/bin/python3
#!/opt/homebrew/bin/python3
# code developed and maintained by (jmw@ruc.edu.cn, RUC, China) date 2025
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, and merge the Software, provided that the following
# conditions are met:
#
# 1. The Software is used for non-commercial purposes only.
# 2. No charge, fee or compensation is given for the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# The above copyright and license must be included in all copies or substantial
# portions of the Software.

import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# Define the input directory and file pattern
input_directory = './'  # Current folder
pattern = '*.1'

# Find all matching files
files = glob.glob(os.path.join(input_directory, pattern))

# Iterate over each file
for file_path in files:
    # Load the data
    data = np.loadtxt(file_path, usecols=(0, 2, 4, 6, 8, 10))

    # Create a figure
    plt.figure(figsize=(10, 6))

    # Plot each column of data
    plt.plot(data[:, 0], data[:, 1], marker='o', markersize =3, label=r'$dz^2$')
    plt.plot(data[:, 0], data[:, 2], marker='o', markersize =3, label=r'$dx^2-y^2$')
    plt.plot(data[:, 0], data[:, 3], marker='o', markersize =3, label=r'$dxz$')
    plt.plot(data[:, 0], data[:, 4], marker='o', markersize =3, label=r'$dyz$')
    plt.plot(data[:, 0], data[:, 5], marker='o', markersize =3, label=r'$dxy$')

    # Set the range of the plot
    plt.xlim([0, 5])
    plt.ylim([-1.2, 0])

    # Add title and legend
    plt.title(fr'{os.path.basename(file_path)}')
    plt.xlabel(r"$i\omega_n$")
    plt.ylabel(r"Im$\Sigma(i\omega_n)$")
    plt.legend()

    # Delete the source file
    os.remove(file_path)

    # Save the figure
    output_filename = f'{os.path.splitext(os.path.basename(file_path))[0]}.png'
    # plt.savefig(output_filename)
    plt.savefig(output_filename+".pdf", bbox_inches='tight')
    plt.close()  # Close the figure to free memory

    print(f'Plot saved as {output_filename}')

print("All plots are generated.")
