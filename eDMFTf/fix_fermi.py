import numpy as np

# Input data
num_orbitals = 5

# Each row: frequency, ReSigma and ImSigma for orbital 1, ReSigma and ImSigma for orbital 2, ..., ReSigma and ImSigma for orbital 5
# Only read first 3 rows of data, skip lines starting with #
data = np.loadtxt('sig.inp.2.1', max_rows=3, comments='#')

# Add data validation
if data.shape[1] != 1 + 2 * num_orbitals:
    raise ValueError(f"Incorrect number of columns. Expected {1 + 2 * num_orbitals} columns, got {data.shape[1]}")

# Extract frequency and self-energy data
omega = data[:, 0]
Re_Sigma = []
Im_Sigma = []

for i in range(num_orbitals):
    Re_Sigma.append(data[:, 1 + i * 2])
    Im_Sigma.append(data[:, 2 + i * 2])

Re_Sigma = np.array(Re_Sigma)  # Shape is (number of orbitals, number of data points)
Im_Sigma = np.array(Im_Sigma)

# Prepare storage for corrected data
Re_Sigma_corrected = Re_Sigma.copy()
Im_Sigma_corrected = Im_Sigma.copy()

# Perform fitting and correction for each orbital
for i in range(num_orbitals):
    try:
        # Fit Im Sigma vs omega^2
        omega_squared = omega[1:] ** 2
        Im_Sigma_i = Im_Sigma[i, 1:]
        # Fit model: Im Sigma = -A * omega^2
        A = np.linalg.lstsq(omega_squared[:, np.newaxis], -Im_Sigma_i, rcond=None)[0][0]
        if A < 0:  # A should be positive physically
            print(f"Warning: Orbital {i+1} has negative A coefficient: {A}")
        
        # Calculate Im Sigma at zero frequency
        Im_Sigma_0 = -A * (omega[0] ** 2)
        Im_Sigma_corrected[i, 0] = Im_Sigma_0

        # Fit Re Sigma vs omega
        omega_fit = omega[1:]
        Re_Sigma_i = Re_Sigma[i, 1:]
        # Fit model: Re Sigma = lambda * omega + Re Sigma(0)
        X = np.column_stack((omega_fit, np.ones(len(omega_fit))))
        lambda_i, Re_Sigma_0 = np.linalg.lstsq(X, Re_Sigma_i, rcond=None)[0]
        # Calculate Re Sigma at zero frequency
        Re_Sigma_corrected[i, 0] = lambda_i * omega[0] + Re_Sigma_0

    except np.linalg.LinAlgError:
        print(f"Warning: Fitting error occurred for orbital {i+1}")
        continue

# Read the entire original file
with open('sig.inp.2.1', 'r') as f:
    all_lines = f.readlines()

# Save to new file, maintaining the original format completely
with open('sig.inp.new', 'w') as f:
    # Write the first two comment lines
    f.write(all_lines[0])
    f.write(all_lines[1])
    
    # Write the corrected data, maintaining the original format completely
    for n in range(len(omega)):
        line = f"{omega[n]:.18e}"
        for i in range(num_orbitals):
            line += f" {Re_Sigma_corrected[i, n]:.18e}"
            line += f" {Im_Sigma_corrected[i, n]:.18e}"
        f.write(line + '\n')
    
    # Write the remaining data lines
    for line in all_lines[len(omega)+2:]:
        f.write(line)

print("\nCorrected data has been saved to sig.inp.new")
print("\n修正后的数据已保存到 sig.inp.new")