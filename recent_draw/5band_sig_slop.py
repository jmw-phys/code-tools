#!/usr/local/bin/python3
# code developed and maintained by (jmw@ruc.edu.cn, RUC, China) date 2025
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

filename = 'Sig.out'

data = np.genfromtxt(filename, delimiter=' ')

# 分别提取x和y数据
x_norg_data = data[:, 0]
y_dz2_norg_data = data[:, 1]
y_dx2_y2_norg_data = data[:, 3]
y_dxz_norg_data = data[:, 5]
y_dyz_norg_data = data[:, 7]
y_dxy_norg_data = data[:, 9]

threshold = 0.1  # 根据你的数据调整这个阈值

def fit_near_zero(x_data, y_data, threshold):
    near_zero_indices = np.abs(x_data) < threshold
    x_near_zero = x_data[near_zero_indices]
    y_near_zero = y_data[near_zero_indices]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_near_zero, y_near_zero)
    return slope, intercept

def plot_fit(x_data, y_data, fit_x, fit_y, slope, label, color):
    plt.figure()  # 每次绘制一个新图
    plt.scatter(x_data, y_data, label=label)
    plt.plot(fit_x, fit_y, '--', label=f'Fit {label}: $m^*$: {1-slope:.4f}', color=color)
    plt.legend()
    plt.title(filename)
    plt.xlabel(r'$\omega$ (eV)')
    plt.ylabel(r'Re[$\Sigma(\omega)$]')
    plt.xlim(-0.2, 0.2)
    plt.ylim(min(y_data) - 0.1 * np.ptp(y_data), max(y_data) + 0.1 * np.ptp(y_data))
    plt.savefig(filename + f'_{label}_Refit.pdf', format='pdf')
    # plt.savefig(filename + f'_{label}_Refit.png')
    plt.close()  # 关闭图以便下次绘制新的图

fit_x = np.linspace(min(x_norg_data), max(x_norg_data), 100)

slope_dz2, intercept_dz2 = fit_near_zero(x_norg_data, y_dz2_norg_data, threshold)
fit_y_dz2 = slope_dz2 * fit_x + intercept_dz2
plot_fit(x_norg_data, y_dz2_norg_data, fit_x, fit_y_dz2, slope_dz2, 'd_{z^2}', 'blue')

slope_dx2_y2, intercept_dx2_y2 = fit_near_zero(x_norg_data, y_dx2_y2_norg_data, threshold)
fit_y_dx2_y2 = slope_dx2_y2 * fit_x + intercept_dx2_y2
plot_fit(x_norg_data, y_dx2_y2_norg_data, fit_x, fit_y_dx2_y2, slope_dx2_y2, 'd_{x^2-y^2}', 'orange')

slope_dxz, intercept_dxz = fit_near_zero(x_norg_data, y_dxz_norg_data, threshold)
fit_y_dxz = slope_dxz * fit_x + intercept_dxz
plot_fit(x_norg_data, y_dxz_norg_data, fit_x, fit_y_dxz, slope_dxz, 'd_{xz}', 'green')

slope_dyz, intercept_dyz = fit_near_zero(x_norg_data, y_dyz_norg_data, threshold)
fit_y_dyz = slope_dyz * fit_x + intercept_dyz
plot_fit(x_norg_data, y_dyz_norg_data, fit_x, fit_y_dyz, slope_dyz, 'd_{yz}', 'red')

slope_dxy, intercept_dxy = fit_near_zero(x_norg_data, y_dxy_norg_data, threshold)
fit_y_dxy = slope_dxy * fit_x + intercept_dxy
plot_fit(x_norg_data, y_dxy_norg_data, fit_x, fit_y_dxy, slope_dxy, 'd_{xy}', 'purple')
