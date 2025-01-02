push!(LOAD_PATH, ENV["ACFLOW_HOME"])
using ACFlow

using DelimitedFiles
using Printf

# Modified function to read all files in a directory and calculate the arithmetic mean of matrices
function read_ctqmc_data(path)
    files = readdir(path)
    all_data = []
    for file in files
        filepath = joinpath(path, file)
        data = readdlm(filepath, Float64)
        push!(all_data, data)
    end

    if length(all_data) == 0
        return nothing
    end

    mean_matrix = zeros(size(all_data[1]))
    for matrix in all_data
        mean_matrix .+= matrix
    end
    mean_matrix ./= length(all_data)
    
    return mean_matrix
end

# Function to group data based on the first column
function group_data(data, nband)
    grouped_data = Dict()
    for row in eachrow(data)
        group_key = row[1]
        values = convert(Vector{Float64}, row[2:end])
        if group_key > nband break end
        push!(get!(grouped_data, group_key, []), values)
    end

    # Convert to Matrix{Float64}
    for (key, value) in grouped_data
        grouped_data[key] = hcat(value...)'
    end
    
    return grouped_data
end

# Function to save data to .data files
function save_data(grouped_data, x)
    for (key, value_matrix) in grouped_data
        # Save only the first x rows
        partial_matrix = value_matrix[1:min(x, end), :]
        filename = "group_$(Int(key)).data"
        open(filename, "w") do io
            for row in eachrow(partial_matrix)
                formatted_row = join([@sprintf("%18.8f", value) for value in row], " ")
                write(io, formatted_row, "\n")
            end
        end
    end
end

# Main function execution (commented out in the original code)
# function main(filepath, x)
#     data = read_ctqmc_data(filepath)
#     grouped_data = group_data(data)
#     save_data(grouped_data, x)
# end

# Run the main function
filepath = "solver.grn"  # Replace with your file path
lent = 102  # Save only the first x rows for each group
nband = 5
# main(filepath, lent)
data = read_ctqmc_data(filepath)
grouped_data = group_data(data, nband)
save_data(grouped_data, lent)

# Get all files in the current directory
files = readdir()
for file in files
    # Check if the file has a .data extension
    if occursin(".data", file)
        # Welcome function (not defined in original code)
        welcome()

        # MaxEnt solver setup parameters
        B = Dict{String,Any}(
            "finput" => file,
            "mtype"  => "flat",
            "mesh"   => "linear",
            "ngrid"  => lent,
            "nmesh"  => 2001,
            "wmax"   => 16.0,
            "wmin"   => -16.0,
            "beta"   => 40.0,
        )

        S = Dict{String,Any}(
            "nalph"  => 16,
            "alpha"  => 1e19,
        )
        
        # Setup parameters (not defined in original code)
        setup_param(B, S)

        # Call the solver (not defined in original code)
        mesh, Aout, Gout = solve(read_data())

        # Move and rename "Aout.data"
        old_Aout_path = "Aout.data"
        
        filename = file
        parts = split(filename, ".")
        prefix = join(parts[1:end-1])

        new_Aout_path = joinpath(prefix * "DOS.txt")
        mv(old_Aout_path, new_Aout_path, force=true) 

        # Remove other generated files
        for generated_file in ["chi2.data", "Gout.data", "model.data", "repr.data"]
            rm(generated_file, force=true)
        end
    end
end
