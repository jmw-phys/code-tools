#!/bin/bash

# 定义目录列表
directories=(
    "2.080-TLoutdz2"
    "2.081-TLoutdx2"
    "2.082-MLdz2"
    "2.083-MLdx2"
    "2.084-TLinndz2"
    "2.085-TLinndx2"
)

# 创建 postprocess-all 文件夹（如果不存在）
mkdir -p postprocess-all

# 遍历每个目录并复制 postprocess
for dir in "${directories[@]}"; do
    cp -r "$dir/postprocess" "postprocess-all/postprocess_${dir}"
done

echo "所有 postprocess 目录已复制到 postprocess-all 文件夹中。"
