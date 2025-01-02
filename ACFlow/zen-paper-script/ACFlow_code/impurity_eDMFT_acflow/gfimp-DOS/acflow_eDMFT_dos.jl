#!/usr/bin/env julia

push!(LOAD_PATH, ENV["ACFLOW_HOME"])
using ACFlow

using DelimitedFiles
using Printf

# 获取当前目录下的所有文件
files = readdir()

# 定义需要提取的列组合和对应的文件名前缀
# columns_and_prefixes = [([1, 2, 7], "1B_"), ([1, 5, 10], "2B_")]
# columns_and_prefixes = [([1, 2, 27], "1B_"), ([1, 8, 33], "2B_"), ([1, 14, 39], "3B_"), ([1, 20, 45], "4B_"), ([1, 26, 51], "5B_")]
# columns_and_prefixes = [([1, 2, 28], "1B_"), ([1, 8, 34], "2B_"), ([1, 14, 40], "3B_"), ([1, 20, 46], "4B_"), ([1, 26, 52], "5B_")]
# columns_and_prefixes = [([1, 2, 5], "WB_"), ([1, 3, 6], "NB_")]
# columns_and_prefixes = [([1, 2, 6], "WB_"), ([1, 3, 7], "NB1_"), ([1, 4, 8], "NB2_")]

columns_and_prefixes = [([1, 2, 3], "eg_"), ([1, 4, 5], "t2g_")]

# 确保 "DOS" 文件夹存在
dos_dir = "DOS"
if !isdir(dos_dir)
    mkdir(dos_dir)
end
lent = 103
for file in files
    # 检查文件是否是 .txt 文件
    if occursin(".txt", file)
        # 读取文件
        data = readdlm(file)

        for (columns, prefix) in columns_and_prefixes
            # 提取指定的列
            new_data = data[1:lent, columns]

            # 添加一列全为0.0001的数据
            rows, cols = size(new_data)
            new_column = fill(0.0001, rows)
            new_data = hcat(new_data, new_column)

            # 格式化数据，保留6位小数
            formatted_data = [@sprintf("%12.8f", val) for val in new_data]

            # 将结果写入新的文件
            # 替换文件后缀为 ".data"
            new_file_name = replace(file, ".txt" => ".data")
            new_file_name = prefix * new_file_name
            # 放入 "DOS" 文件夹中
            new_file_name = joinpath(dos_dir, new_file_name)
            writedlm(new_file_name, formatted_data)

            welcome()

# MaxEnt solver Setup parameters
            B = Dict{String,Any}(
                "finput" => new_file_name,
                # "mtype"  => "gauss",
                "mtype"  => "flat",
                "mesh"   => "linear",
                "ngrid"  => lent,
                "nmesh"  => 2001,
                "wmax"   => 16.0,
                "wmin"   => -16.0,
                "beta"   => 40.0,
            )

            S = Dict{String,Any}(
                "nalph"  => 15,
                "alpha"  => 1e15,
            )

#=
# StochOM solver Setup parameters
            B = Dict{String,Any}(
                "finput"  =>  new_file_name,
                "solver"  => "StochOM"
                "ktype"   => "fermi"
                "mtype"   => "flat"
                "grid"    => "ffreq"
                "mesh"    => "linear"
                "ngrid"   => 10
                "nmesh"   => 501
                "wmax"    => 5.0
                "wmin"    => -5.0
                "beta"    =>  314.159265358979323,
                "offdiag" => false
            )

            S = Dict{String,Any}(
                "ntry"   => 10000
                "nstep"  => 1000
                "nbox"   => 100
                "sbox"   => 0.005
                "wbox"   => 0.02
                "norm"   => -1.0
            )
=#

            setup_param(B, S)

            # Call the solver
            mesh, Aout, Gout = solve(read_data())

            # Move and rename "Aout.data"
            old_Aout_path = "Aout.data"
            # new_Aout_path = joinpath("DOS", prefix * "Aout.data")
            new_Aout_path = joinpath(dos_dir, prefix * replace(file, "mb.gfimp.txt" => "Aout.txt"))
            cp(old_Aout_path, new_Aout_path, force=true) # force=true 会覆盖同名的目标文件

            # copy other generated files
            for generated_file in ["Aout.data", "chi2.data", "Gout.data", "model.data", "repr.data"]
                new_file = prefix * generated_file
                cp(generated_file, new_file, force=true)
            end
        end
    end
end
