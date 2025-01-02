#!/usr/bin/env julia

push!(LOAD_PATH, ENV["ACFLOW_HOME"])
using ACFlow
using DelimitedFiles
using Printf

# 获取当前目录下的所有.txt文件
txt_files = filter(x -> occursin(".txt", x), readdir())

# 确保 "sgm" 文件夹存在
sgm_dir = "SGM"
if !isdir(sgm_dir)
    mkdir(sgm_dir)
end

lent = 103
max_lent = 1909
# columns_and_prefixes = [
#     ([1, 2, 28], "1B_"),
#     ([1, 8, 34], "2B_"),
#     ([1, 14, 40], "3B_"),
#     ([1, 20, 46], "4B_"),
#     ([1, 26, 52], "5B_")
# ]

columns_and_prefixes = [([1, 2, 3], "eg_"), ([1, 4, 5], "t2g_")]


# 提取和处理数据函数
function process_data(file, columns, prefix)
    data = readdlm(file)
    new_data = data[1:max_lent, columns]
    new_data = hcat(new_data, fill(0.0001, size(new_data, 1)), fill(0.0001, size(new_data, 1)))
    formatted_data = [@sprintf("%12.8f", val) for val in new_data]
    new_file_name = joinpath(sgm_dir, prefix * replace(file, ".txt" => ".data"))
    writedlm(new_file_name, formatted_data)

    # Read self-energy function
    dlm = readdlm(new_file_name)
    #
    # Get grid
    grid = dlm[1:lent,1]
    #
    # Get self-energy function
    Σinp = dlm[1:lent,2] + im * dlm[1:lent,3] # Value part
    Σerr = dlm[1:lent,4] + im * dlm[1:lent,5] # Error part
    #
    # Subtract hartree term
    Σ∞ = dlm[max_lent,2]
    @. Σinp = Σinp - Σ∞

    print("Σ∞ = $(Σ∞)\n")

    welcome()
    
    B = Dict{String,Any}(
        "solver" => "MaxEnt",  # Choose MaxEnt solver
        "mtype"  => "gauss",   # Default model function
        "mesh"   => "tangent", # Mesh for spectral function
        "ngrid"  => lent,
        "nmesh"  => 1601,
        "wmax"   => 16.0,
        "wmin"   => -16.0,
        "beta"   => 40.0
    )
    
    S = Dict{String,Any}(
        "nalph"  => 15,
        "alpha"  => 1e15
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
    new_sigma_path = joinpath(sgm_dir, prefix * replace(file, ".data" => ".txt"))

    cp(old_sigma_path, new_sigma_path, force=true) # force=true 会覆盖同名的目标文件
    
    # copy other generated files
    for generated_file in ["Aout.data", "chi2.data", "Gout.data", "model.data", "repr.data"]
        new_file = prefix * generated_file
        cp(generated_file, new_file, force=true)
    end
end

# 主程序
for file in txt_files
    for (columns, prefix) in columns_and_prefixes
        process_data(file, columns, prefix)
    end
end
