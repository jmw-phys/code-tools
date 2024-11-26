#!/usr/local/bin/python3
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
y_dxy_norg_data = data[:, 9]
y_dyz_norg_data = data[:, 7]

threshold = 0.01 # 根据你的数据调整这个阈值

def fit_near_zero(x_data, y_data, threshold):
    near_zero_indices = np.abs(x_data) < threshold
    x_near_zero = x_data[near_zero_indices]
    y_near_zero = y_data[near_zero_indices]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_near_zero, y_near_zero)
    return slope, intercept

# 删除原来的plot_fit函数，改为新的绘图方式
plt.figure(figsize=(10, 6))  # 创建一个更大的图

fit_x = np.linspace(min(x_norg_data), max(x_norg_data), 100)

# dz2
slope_dz2, intercept_dz2 = fit_near_zero(x_norg_data, y_dz2_norg_data, threshold)
fit_y_dz2 = slope_dz2 * fit_x + intercept_dz2
plt.scatter(x_norg_data, y_dz2_norg_data, label=f'd_{{z^2}}', alpha=0.5)
plt.plot(fit_x, fit_y_dz2, '--', label=f'd_{{z^2}} fit: $m^*$: {1-slope_dz2:.4f}')

# dx2-y2
slope_dx2_y2, intercept_dx2_y2 = fit_near_zero(x_norg_data, y_dx2_y2_norg_data, threshold)
fit_y_dx2_y2 = slope_dx2_y2 * fit_x + intercept_dx2_y2
plt.scatter(x_norg_data, y_dx2_y2_norg_data, label=f'd_{{x^2-y^2}}', alpha=0.5)
plt.plot(fit_x, fit_y_dx2_y2, '--', label=f'd_{{x^2-y^2}} fit: $m^*$: {1-slope_dx2_y2:.4f}')

# dxz
slope_dxz, intercept_dxz = fit_near_zero(x_norg_data, y_dxz_norg_data, threshold)
fit_y_dxz = slope_dxz * fit_x + intercept_dxz
plt.scatter(x_norg_data, y_dxz_norg_data, label=f'd_{{xz}}', alpha=0.5)
plt.plot(fit_x, fit_y_dxz, '--', label=f'd_{{xz}} fit: $m^*$: {1-slope_dxz:.4f}')

# dyz
slope_dyz, intercept_dyz = fit_near_zero(x_norg_data, y_dyz_norg_data, threshold)
fit_y_dyz = slope_dyz * fit_x + intercept_dyz
plt.scatter(x_norg_data, y_dyz_norg_data, label=f'd_{{yz}}', alpha=0.5)
plt.plot(fit_x, fit_y_dyz, '--', label=f'd_{{yz}} fit: $m^*$: {1-slope_dyz:.4f}')

# dxy
slope_dxy, intercept_dxy = fit_near_zero(x_norg_data, y_dxy_norg_data, threshold)
fit_y_dxy = slope_dxy * fit_x + intercept_dxy
plt.scatter(x_norg_data, y_dxy_norg_data, label=f'd_{{xy}}', alpha=0.5)
plt.plot(fit_x, fit_y_dxy, '--', label=f'd_{{xy}} fit: $m^*$: {1-slope_dxy:.4f}')

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.title(f'{filename} (threshold: {threshold})')
plt.xlabel(r'$\omega$ (eV)')
plt.ylabel(r'Re[$\Sigma(\omega)$]')
plt.xlim(-0.2, 0.2)
plt.ylim(-2.5, 2.5)
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()  # 自动调整布局

# 保存图片
plt.savefig(filename + f'_all_bands_fit.pdf', format='pdf', bbox_inches='tight')
plt.close()
