using DelimitedFiles
using Printf

# Modified function to read all files in a directory and calculate the arithmetic mean of matrices
function read_files(path)
    files = readdir(path)
    all_data = Array{Array{Float64,2},1}()  # Explicitly define all_data type
    for file in files
        filepath = joinpath(path, file)
        data = readdlm(filepath)[2:8194,:]  # Assuming data structure aligns with the example
        push!(all_data, data)
    end

    if isempty(all_data)
        return nothing
    end

    mean_matrix = zeros(size(all_data[1]))
    for matrix in all_data
        mean_matrix .+= matrix
    end
    mean_matrix ./= length(all_data)
    
    return mean_matrix
end

dirpath = "src.giw"  # Replace with your directory path

data = read_files(dirpath)
if data === nothing
    println("No data to process.")
    return
end

# The output filename is based on the directory name
output_filename = "average_of_$(basename(dirpath)).txt"
open(output_filename, "w") do io
    for row in eachrow(data)
        # Write the frequency value (assuming it is the first element of each row)
        write(io, @sprintf("%23.16E", row[1]))

        # Write Re values
        for i in 2:26  # Adjust range according to your data structure
            write(io, " ", @sprintf("%23.16E", row[i]))
        end

        # Write Im values (assuming they follow Re values in the same row)
        for i in 27:51  # Adjust range according to your data structure
            write(io, " ", @sprintf("%23.16E", row[i]))
        end

        # New line after each row
        write(io, "\n")
    end
end
