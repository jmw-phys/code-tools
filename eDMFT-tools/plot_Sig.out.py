#!/usr/bin/env python3
# code developed and maintained by (jmw@ruc.edu.cn, RUC, China) date 2025
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import argparse

def plot_signal_file(filename, groups_to_plot=[1, 2, 3]):
    # Read data file
    try:
        data = np.loadtxt(filename)
    except Exception as e:
        print(f"Cannot read file {filename}: {e}")
        return
    
    # Check if there are enough columns
    if data.shape[1] >= 19:  # Ensure at least 19 columns (index 0-18)
        plots_created = []
        
        # First group - Diagonal elements (2,10,18)
        if 1 in groups_to_plot:
            plt.figure(figsize=(10, 6))
            plt.plot(data[:, 0], data[:, 2], label='Diagonal (2)', color='blue')
            plt.plot(data[:, 0], data[:, 10], label='Diagonal (10)', color='red')
            plt.plot(data[:, 0], data[:, 18], label='Diagonal (18)', color='green')
            plt.xlim(0, 5)
            # plt.ylim(-2, 0)
            plt.title(f'Diagonal Elements - {os.path.basename(filename)}')
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.legend()
            plt.grid(True)
            plt.savefig(f"group1_{filename}.png", dpi=300)
            plt.close()
            plots_created.append(f"group1_{filename}.png")
        
        # Second group - Upper elements (4,6,12)
        if 2 in groups_to_plot:
            plt.figure(figsize=(10, 6))
            plt.plot(data[:, 0], data[:, 4], label='Upper (4)', color='blue')
            plt.plot(data[:, 0], data[:, 6], label='Upper (6)', color='red')
            plt.plot(data[:, 0], data[:, 12], label='Upper (12)', color='green')
            plt.xlim(0, 5)
            # plt.ylim(-0.2, 0)
            plt.title(f'Upper Elements - {os.path.basename(filename)}')
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.legend()
            plt.grid(True)
            plt.savefig(f"group2_{filename}.png", dpi=300)
            plt.close()
            plots_created.append(f"group2_{filename}.png")
        
        # Third group - Lower elements (8,14,16)
        if 3 in groups_to_plot:
            plt.figure(figsize=(10, 6))
            plt.plot(data[:, 0], data[:, 8], label='Lower (8)', color='blue')
            plt.plot(data[:, 0], data[:, 14], label='Lower (14)', color='red')
            plt.plot(data[:, 0], data[:, 16], label='Lower (16)', color='green')
            plt.xlim(0, 5)
            # plt.ylim(-0.2, 0)
            plt.title(f'Lower Elements - {os.path.basename(filename)}')
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.legend()
            plt.grid(True)
            plt.savefig(f"group3_{filename}.png", dpi=300)
            plt.close()
            plots_created.append(f"group3_{filename}.png")
        
        if plots_created:
            print(f"Charts saved to: {', '.join(plots_created)}")
    else:
        print(f"Warning: {filename} has insufficient columns, only {data.shape[1]} columns")
        # Plot as many columns as possible based on selected groups
        plots_created = []
        
        if 1 in groups_to_plot and data.shape[1] > 2:
            plt.figure(figsize=(10, 6))
            plt.plot(data[:, 0], data[:, 2], label='Diagonal (2)', color='blue')
            if data.shape[1] > 10:
                plt.plot(data[:, 0], data[:, 10], label='Diagonal (10)', color='red')
            if data.shape[1] > 18:
                plt.plot(data[:, 0], data[:, 18], label='Diagonal (18)', color='green')
            plt.xlim(0, 5)
            plt.ylim(-2, 0)
            plt.title(f'Diagonal Elements - {os.path.basename(filename)}')
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.legend()
            plt.grid(True)
            plt.savefig(f"group1_{filename}.png", dpi=300)
            plt.close()
            plots_created.append(f"group1_{filename}.png")
        
        if 2 in groups_to_plot and data.shape[1] > 4:
            plt.figure(figsize=(10, 6))
            plt.plot(data[:, 0], data[:, 4], label='Upper (4)', color='blue')
            if data.shape[1] > 6:
                plt.plot(data[:, 0], data[:, 6], label='Upper (6)', color='red')
            if data.shape[1] > 12:
                plt.plot(data[:, 0], data[:, 12], label='Upper (12)', color='green')
            plt.xlim(0, 5)
            plt.ylim(-2, 0)
            plt.title(f'Upper Elements - {os.path.basename(filename)}')
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.legend()
            plt.grid(True)
            plt.savefig(f"group2_{filename}.png", dpi=300)
            plt.close()
            plots_created.append(f"group2_{filename}.png")
        
        if 3 in groups_to_plot and data.shape[1] > 8:
            plt.figure(figsize=(10, 6))
            plt.plot(data[:, 0], data[:, 8], label='Lower (8)', color='blue')
            if data.shape[1] > 14:
                plt.plot(data[:, 0], data[:, 14], label='Lower (14)', color='red')
            if data.shape[1] > 16:
                plt.plot(data[:, 0], data[:, 16], label='Lower (16)', color='green')
            plt.xlim(0, 5)
            plt.ylim(-2, 0)
            plt.title(f'Lower Elements - {os.path.basename(filename)}')
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.legend()
            plt.grid(True)
            plt.savefig(f"group3_{filename}.png", dpi=300)
            plt.close()
            plots_created.append(f"group3_{filename}.png")
        
        if plots_created:
            print(f"Charts saved to: {', '.join(plots_created)}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Plot signal data with group selection')
    parser.add_argument('--groups', type=int, nargs='+', default=[1, 2, 3],
                        help='Groups to plot: 1=Diagonal, 2=Upper, 3=Lower. Default: all groups')
    args = parser.parse_args()
    
    # Find all matching files, excluding PNG files
    files = [f for f in glob.glob("*.inp.*") if not f.endswith('.png')]
    
    if not files:
        print("No matching files '*.inp.*' found")
        return
    
    print(f"Found {len(files)} files to process...")
    print(f"Selected groups to plot: {', '.join(['Diagonal' if 1 in args.groups else '', 'Upper' if 2 in args.groups else '', 'Lower' if 3 in args.groups else ''])}")
    
    # Process each file
    for filename in sorted(files):
        print(f"Processing file: {filename}")
        plot_signal_file(filename, args.groups)
    
    print("All files processing completed!")

if __name__ == "__main__":
    main() 
