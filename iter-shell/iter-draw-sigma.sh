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

# 遍历每个目录
for dir in "${directories[@]}"; do
    cd "$dir/postprocess"
    gnuplot << EOF
set terminal pdfcairo enhanced font 'Helvetica,10' transparent
set output "plot-eta-0p001.pdf"
plot "Sigmaout-eta-0p001.data" using 1:2 with lines, "" using 1:3 with lines
EOF
    cd -
done
