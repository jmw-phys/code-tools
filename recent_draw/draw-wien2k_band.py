#!/opt/homebrew/bin/python3
# code developed and maintained by (jmw@ruc.edu.cn, RUC, China) date 2025
##!/usr/local/bin/python3

import numpy as np
import matplotlib.pyplot as plt

def parse_wien2k_band(file_path):
    """
    解析Wien2k能带数据文件，提取每个能带的第4列和第5列数据。
    
    参数：
        file_path (str): 数据文件路径。
    
    返回：
        bands (dict): 字典，键为能带索引，值为包含'x'和'y'数据的字典。
    """
    bands = {}
    current_band = None
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('bandindex'):
                # 获取当前能带索引
                current_band = int(line.split(':')[1].strip())
                bands[current_band] = {'x': [], 'y': []}
            elif line and not line.startswith('#') and current_band is not None:
                parts = line.split()
                if len(parts) >= 5:
                    try:
                        x = float(parts[3])  # 第4列
                        y = float(parts[4])  # 第5列
                        bands[current_band]['x'].append(x)
                        bands[current_band]['y'].append(y)
                    except ValueError:
                        # 如果转换失败，跳过该行
                        continue
    return bands

def plot_bands(bands, horizontal_energy=0, horizontal_color='black', horizontal_style='--', horizontal_width=1):
    """
    绘制能带图，并在指定的能量位置添加水平线。
    
    参数：
        bands (dict): 解析后的能带数据。
        horizontal_energy (float): 要添加水平线的能量值。
        horizontal_color (str): 水平线颜色。
        horizontal_style (str): 水平线样式，如 '--', '-.', ':' 等。
        horizontal_width (float): 水平线宽度。
    """
    plt.figure(figsize=(10, 6))
    
    for band_index, data in bands.items():
        plt.plot(data['x'], data['y'])
    
    # 添加水平线
    plt.axhline(y=horizontal_energy, color=horizontal_color, linestyle=horizontal_style, linewidth=horizontal_width)
    
    # 设置高对称点的位置和标签（根据具体情况调整）
    # 这里假设高对称点在特定的x位置
    # 例如，如果高对称点对应于x=0, x=0.5, x=1.0等
    # 您需要根据实际数据调整这些值

    high_symmetry_x = np.array([0, 70, 117, 187, 302, 349, 464, 585, 632, 754, 800])
    scale_factor = 3.85445 / 801
    high_symmetry_x = high_symmetry_x * scale_factor
    high_symmetry_labels = [r'$\Gamma$', 'Y', 'T', 'Z', 'M', 'N', r'$\Gamma$', 'X', 'A', 'Z', r'$\Gamma$']
    plt.xticks(high_symmetry_x, high_symmetry_labels)
    
    plt.xlabel('K point')
    plt.ylim(-2, 5)
    plt.xlim(0, 3.85445)
    plt.ylabel('Energy (eV)')
    plt.title('Wien2k band structure')
    # plt.legend()  # 已移除图例
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 主程序
if __name__ == "__main__":
    data_file = 'lda.spaghetti_ene'  # 替换为您的数据文件路径
    bands = parse_wien2k_band(data_file)
    
    # 检查解析结果
    if not bands:
        print("Error: No band data parsed. Please check the data file format.")
    else:
        # 绘制能带图，并在能量为0的位置添加水平线
        plot_bands(bands, horizontal_energy=0, horizontal_color='black', horizontal_style='--', horizontal_width=1)
