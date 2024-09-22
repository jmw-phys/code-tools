#!/bin/bash

# 定义需要处理的目录列表
directories=(
    "2.082-MLdz2"
    "2.083-MLdx2"
    "2.084-TLinndz2"
    "2.085-TLinndx2"
)

# 遍历每个目录
for dir in "${directories[@]}"; do
    # 构建 postprocess 目录的路径
    postprocess_dir="${dir}/postprocess"
    
    # 检查 postprocess 目录是否存在
    if [ -d "$postprocess_dir" ]; then
        echo "进入目录: $postprocess_dir"
        
        # 进入 postprocess 目录
        cd "$postprocess_dir" || { echo "无法进入目录 $postprocess_dir"; continue; }
        
        # 执行 Julia 脚本
        julia ../../Postprocess-pole.data-v2.jl
        
        # 检查 Julia 命令是否执行成功
        if [ $? -eq 0 ]; then
            echo "成功执行 Julia 脚本在 $postprocess_dir"
        else
            echo "在 $postprocess_dir 执行 Julia 脚本时出错"
        fi
        
        # 返回上一级目录
        cd - > /dev/null
    else
        echo "目录不存在: $postprocess_dir"
    fi
done

echo "所有任务完成。"
