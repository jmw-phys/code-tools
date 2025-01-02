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
filepath = "solver.sgm"  # Replace with your file path
lent = 102  # Save only the first x rows for each group
nband = 5
# main(filepath, lent)
data = read_ctqmc_data(filepath)
grouped_data = group_data(data, nband)
save_data(grouped_data, 8193)

# 获取当前目录下的所有文件
files = readdir()
for file in files
    # 检查文件是否是 .txt 文件
    if occursin(".data", file)
        welcome()

        # Read self-energy function
        dlm = readdlm(file)
        #
        # Get grid
        grid = dlm[1:lent,1]
        #
        # Get self-energy function
        Σinp = dlm[1:lent,2] + im * dlm[1:lent,3] # Value part
        Σerr = dlm[1:lent,4] + im * dlm[1:lent,5] # Error part
        #
        # Subtract hartree term
        Σ∞ = dlm[8193,2]
        @. Σinp = Σinp - Σ∞





        # MaxEnt solver Setup parameters
                    B = Dict{String,Any}(
                        # "finput" => file,
                        # "mtype"  => "gauss",
                        "solver" => "MaxEnt",  # Choose MaxEnt solver
                        "mtype"  => "flat",
                        "mesh"   => "linear",
                        "ngrid"  => lent,
                        "nmesh"  => 2001,
                        "wmax"   => 20.0,
                        "wmin"   => -20.0,
                        "beta"   => 40.0,
                    )

            S = Dict{String,Any}(
                "nalph"  => 16,
                "alpha"  => 1e16,
            )
            
        setup_param(B, S)

        # Call the solver
        mesh, Aout, Σout = solve(grid, Σinp, Σerr)

        # Calculate final self-energy function on real axis
        #
        # Construct final self-energy function
        @. Σout = Σout + Σ∞
        #
        # Write self-energy function to sigma.data
        open("sigma.data", "w") do fout
            for i in eachindex(mesh)
                z = Σout[i]
                @printf(fout, "%20.16f %20.16f %20.16f\n", mesh[i], real(z), imag(z))
            end
        end

        old_sigma_path = "sigma.data"
        
        filename = file
        parts = split(filename, ".")  # 使用点号作为分隔符
        prefix = join(parts[1:end-2])  # 把所有部分（除了最后一个）连接起来

        # new_Aout_path = joinpath("DOS", prefix * "Aout.data")
        # new_Aout_path = joinpath(dos_dir, prefix * replace(file, "mb.gfimp.txt" => "Aout.txt"))
        new_sigma_path = joinpath( prefix * "sigma.txt")
        mv(old_sigma_path, new_sigma_path, force=true) # force=true 会覆盖同名的目标文件

        # Remove other generated files
        for generated_file in ["Aout.data", "chi2.data", "Gout.data", "model.data", "repr.data"]
            rm(generated_file, force=true) # force=true 会忽略不存在的文件
        end
    end
end

