
push!(LOAD_PATH, ENV["ACFLOW_HOME"])
using ACFlow

using DelimitedFiles
using Printf

# 读取数据
function read_ctqmc_data(filepath)
    return readdlm(filepath, Float64)
end

# 将数据按照第一列分组
function group_data(data, nband)
    grouped_data = Dict()
    for row in eachrow(data)
        group_key = row[1]
        values = convert(Vector{Float64}, row[2:end])
        if group_key > nband break end
        push!(get!(grouped_data, group_key, []), values)
    end

    # 转换为 Matrix{Float64}
    for (key, value) in grouped_data
        grouped_data[key] = hcat(value...)'
    end
    
    return grouped_data
end



# 保存数据到 .data 文件
function save_data(grouped_data, x)
    for (key, value_matrix) in grouped_data
        # 只保存前 x 行
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


# 主函数
# function main(filepath, x)
#     data = read_ctqmc_data(filepath)
#     grouped_data = group_data(data)
#     save_data(grouped_data, x)
# end

# 执行主函数
filepath = "solver.grn.dat"  # 替换为你的文件路径
lent = 102  # 只保存每组的前 x 行
nband = 5
# main(filepath, lent)
data = read_ctqmc_data(filepath)
grouped_data = group_data(data, nband)
save_data(grouped_data, lent)

# 获取当前目录下的所有文件
files = readdir()
for file in files
    # 检查文件是否是 .txt 文件
    if occursin(".data", file)
        welcome()

        # MaxEnt solver Setup parameters
                    B = Dict{String,Any}(
                        "finput" => file,
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
                "nalph"  => 16,
                "alpha"  => 1e16,
            )
            
        setup_param(B, S)

        # Call the solver
        mesh, Aout, Gout = solve(read_data())

        # Move and rename "Aout.data"
        old_Aout_path = "Aout.data"
        
        filename = file
        parts = split(filename, ".")  # 使用点号作为分隔符
        prefix = join(parts[1:end-1])  # 把所有部分（除了最后一个）连接起来

        # new_Aout_path = joinpath("DOS", prefix * "Aout.data")
        # new_Aout_path = joinpath(dos_dir, prefix * replace(file, "mb.gfimp.txt" => "Aout.txt"))
        new_Aout_path = joinpath( prefix * "DOS.txt")
        # new_Aout_path = joinpath(dos_dir, replace(file, "mb.gfimp.txt" => "Aout.txt"))
        mv(old_Aout_path, new_Aout_path, force=true) # force=true 会覆盖同名的目标文件

        # Remove other generated files
        for generated_file in ["chi2.data", "Gout.data", "model.data", "repr.data"]
            rm(generated_file, force=true) # force=true 会忽略不存在的文件
        end
    end
end