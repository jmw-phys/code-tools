#!/bin/bash


# This file is mainly used for submitting jobs on bohr
suffix=$(basename $PWD | cut -c 1-4)
sbatch --export=suffix=$suffix <<EOT
#!/bin/bash
#SBATCH -J STOC${suffix}
#SBATCH -p batch
#SBATCH -N 1 --ntasks-per-node 64
#SBATCH --time=2-0:0:0
##SBATCH --reservation=jm_reservation
#SBATCH --mem=224G
##SBATCH -d afterok:287
#SBATCH -o out.%j
#SBATCH -e err.%j


export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export FI_PROVIDER=verbs
export UCX_NET_DEVICES=mlx5_0:1

# cd $SLURM_SUBMIT_DIR
# scontrol show hostname $SLURM_NODELIST > host.txt

julia ./sgm_stochpx.jl > nohup.dat 2>&1
EOT
