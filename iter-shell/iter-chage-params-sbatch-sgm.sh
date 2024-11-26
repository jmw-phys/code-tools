#!/bin/bash

# 循环从0到5
#for x in {0..5}
for x in 0 2
do
    # 定义目录名称
    dir="idx-$x"

    # 创建目录
    mkdir "$dir"

    # 复制文件到新目录
    cp giw_stochpx.jl Gf.out "$dir/"

    # 修改 sgm_stochpx.jl 文件的第37行
    # 使用sed命令替换第37行内容为 "band_idx = $x"
    sed -i "37s/.*/band_idx = $x/" "$dir/sgm_stochpx.jl"

    # 进入新目录并执行source命令
    (
        cd "$dir" || exit
        source ~/jm_script/jmrun-sgm-stochPX.sh
    )
done
