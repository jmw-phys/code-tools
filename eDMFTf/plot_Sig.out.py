#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

def plot_signal_file(filename):
    # Read data file
    try:
        data = np.loadtxt(filename)
    except Exception as e:
        print(f"Cannot read file {filename}: {e}")
        return
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Check if there are enough columns
    if data.shape[1] >= 19:  # Ensure at least 19 columns (index 0-18)
        plt.plot(data[:, 0], data[:, 2], label='Column 3')
        plt.plot(data[:, 0], data[:, 10], label='Column 11')
        plt.plot(data[:, 0], data[:, 18], label='Column 19')
    else:
        print(f"Warning: {filename} has insufficient columns, only {data.shape[1]} columns")
        # Plot as many columns as possible
        if data.shape[1] > 2:
            plt.plot(data[:, 0], data[:, 2], label='Column 3')
        if data.shape[1] > 10:
            plt.plot(data[:, 0], data[:, 10], label='Column 11')
    
    # Set x-axis range to [0:10]
    plt.xlim(0, 5)
    
    # Add title and labels
    plt.title(f'Data Visualization: {os.path.basename(filename)}')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid(True)
    
    # Save as PNG, keep complete filename
    output_filename = f"{filename}.png"
    plt.savefig(output_filename, dpi=300)
    plt.close()
    print(f"Chart saved to: {output_filename}")

def main():
    # Find all matching files, excluding PNG files
    files = [f for f in glob.glob("Sig.out.*") if not f.endswith('.png')]
    
    if not files:
        print("No matching files 'Sig.out.*' found")
        return
    
    print(f"Found {len(files)} files to process...")
    
    # Process each file
    for filename in sorted(files):
        print(f"Processing file: {filename}")
        plot_signal_file(filename)
    
    print("All files processing completed!")

if __name__ == "__main__":
    main() 