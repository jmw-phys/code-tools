
# code developed and maintained by (jmw@ruc.edu.cn, RUC, China) date 2025
using Statistics
using LinearAlgebra
using Printf

# Define the Pole structure
struct Pole
    P_i::Float64
    A_i::Float64
    sign_i::Float64
end

# Define the Block structure
struct Block
    chi2::Float64
    poles::Vector{Pole}
end

function parse_pole_data(file_path::String)::Vector{Block}
    """
    Parse the pole.data file and return a list containing all blocks.
    Each block is a Block struct containing chi2 and pole data.
    """
    blocks = Block[]  # Initialize an empty vector of Block
    current_block = nothing  # Placeholder for the current block
    poles = Pole[]  # Initialize an empty vector of Pole

    # Define the regex pattern for chi2
    chi2_pattern = r"χ²:\s*([0-9.eE+-]+)"

    open(file_path, "r") do file
        for line in eachline(file)
            line = strip(line)
            if startswith(line, "# Try")
                if current_block !== nothing
                    # Assign the collected poles to the current block and push to blocks
                    current_block = Block(current_block.chi2, copy(poles))
                    push!(blocks, current_block)
                    current_block = nothing
                    empty!(poles)  # Clear the poles vector for the next block
                end
                # Use regular expressions to extract chi2
                m = match(chi2_pattern, line)
                if m !== nothing
                    chi2_value = parse(Float64, m.captures[1])
                    current_block = Block(chi2_value, Pole[])
                end
            elseif !isempty(line) && !startswith(line, "#")
                parts = split(line)
                if length(parts) >= 5
                    # Extract P_i (3rd column), A_i (4th column), sign_i (5th column)
                    P_i = parse(Float64, parts[3])
                    A_i = parse(Float64, parts[4])
                    sign_i = parse(Float64, parts[5])
                    pole = Pole(P_i, A_i, sign_i)
                    push!(poles, pole)
                end
            end
        end
    end

    # Add the last block if it exists
    if current_block !== nothing
        current_block = Block(current_block.chi2, copy(poles))
        push!(blocks, current_block)
    end

    return blocks
end

function filter_blocks(blocks::Vector{Block})::Vector{Block}
    """
    Filter out blocks with chi2 greater than the median.
    """
    chi2_values = [block.chi2 for block in blocks]
    median_chi2 = median(chi2_values)
    filtered_blocks = filter(block -> block.chi2 <= median_chi2, blocks)
    println("Total blocks: ", length(blocks), ", Filtered blocks: ", length(filtered_blocks))
    return filtered_blocks
end

function compute_green_function(blocks::Vector{Block}, omegas::Vector{Float64}, eta::Float64)::Vector{ComplexF64}
    """
    Compute the average Green function G(omega) for each omega.
    G(omega) = sum_i (A_i * sign_i) / (omega - P_i + i eta)
    """
    G_avg = zeros(ComplexF64, length(omegas))
    total_blocks = length(blocks)
    for (block_idx, block) in enumerate(blocks)
        for pole in block.poles
            numerator = pole.A_i * pole.sign_i
            denominator = omegas .- pole.P_i .+ im * eta
            G_avg .+= numerator ./ denominator
        end
        if (block_idx % 100 == 0) || (block_idx == total_blocks)
            println("Processed ", block_idx, " / ", total_blocks, " blocks")
        end
    end
    G_avg ./= total_blocks
    return G_avg
end

"""
write_complex_data(am::Vector{Float64}, data::Vector{ComplexF64}, filename::String)

Write complex data to a specified file. The grid is defined in `am`, and
the complex data are contained in `data`.

### Arguments
* `am`       -> Real frequency mesh.
* `data`     -> Complex data (e.g., Green function or Sigma).
* `filename` -> Output filename.

### Returns
N/A
"""
function write_complex_data(am::Vector{Float64}, data::Vector{ComplexF64}, filename::String)
    @assert length(am) == length(data)

    open(filename, "w") do fout
        for i in eachindex(am)
            @printf(fout, "%16.12f %16.12f %16.12f\n", am[i], real(data[i]), imag(data[i]))
        end
    end
end

function main()
    # Configure parameters
    pole_data_file = "../pole.data"    # Path to pole.data file

    # Step 1: Parse the pole.data file
    blocks = parse_pole_data(pole_data_file)
    println("Parsed ", length(blocks), " blocks.")

    # Step 2: Filter blocks
    filtered_blocks = filter_blocks(blocks)

    # Step 3: Generate omega range
    omega_start = -15.0
    omega_end = 15.0
    omega_step = 0.01
    omegas = collect(omega_start:omega_step:omega_end)  # Include endpoint
    println("Generated ", length(omegas), " omega points, from ", omega_start, " to ", omega_end, ", step ", omega_step)

    # Define the list of eta values
    eta_values = [0.1, 0.01, 0.001]

    for eta in eta_values
        println("\nProcessing eta = ", eta)
        # Step 4: Compute the average Green function G(omega) for the current eta
        G_avg = compute_green_function(filtered_blocks, omegas, eta)

        # Step 5: Compute Sigmaout = (omegas - 1.0 ./ G_avg)
        Sigma_out = omegas .- (1.0 ./ G_avg)

        # Step 6: Write the Green function to the corresponding output file
        # Format eta to avoid issues in filenames (replace '.' with 'p')
        eta_str = replace(string(eta), "." => "p")
        gout_filename = "Gout-eta-$(eta_str).data"
        write_complex_data(omegas, G_avg, gout_filename)
        println("Green function for eta = ", eta, " has been saved to ", gout_filename)

        # Step 7: Write the Sigma function to the corresponding output file
        sigmaout_filename = "Sigmaout-eta-$(eta_str).data"
        write_complex_data(omegas, Sigma_out, sigmaout_filename)
        println("Sigma function for eta = ", eta, " has been saved to ", sigmaout_filename)
    end
end

# Execute the main function
main()