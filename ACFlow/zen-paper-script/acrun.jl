#!/usr/bin/env julia

#
# This script is used to start analytical continuation simulations.
# It will launch only 1 process.
#
# Usage:
#
#     $ acrun.jl ac.toml
####################################################################
# This file is mainly used for submitting jobs on bohr for DOS

push!(LOAD_PATH, ENV["ACFLOW_HOME"])

# using ACFlow

using Distributed
addprocs(63)

@everywhere using ACFlow
welcome()
overview()
read_param()
solve(read_data())
# goodbye()
