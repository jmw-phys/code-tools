using LinearAlgebra
using Printf


# Define atom coordinates - only need to modify these three lines to define local coordinate system
pCenter = [0.24824, 0.24644, 0.50000]  # central atom position
pAxis1 = [0.50225, 0.49775, 0.50000]   # atom defining the a-axis direction
pAxis2 = [0.24845, 0.24671, 0.64663]   # atom defining the b-axis direction

# Define axis vectors
va = pAxis1 .- pCenter  # vector for a-axis
vb = pAxis2 .- pCenter  # vector for b-axis

# Orthonormal basis
# a-axis unit vector
e1 = va / norm(va)
# Project vb onto plane orthogonal to e1 and normalize
e2 = (vb .- dot(vb, e1) * e1) / norm(vb .- dot(vb, e1) * e1)
# c-axis from right-hand rule
e3 = cross(e1, e2)
e3 /= norm(e3)

# Rotation matrix (rows are new axis directions)
R = vcat(e1', e2', e3')

# Output rotation matrix
@printf("Rotation matrix R = \n")
for row in eachrow(R)
    @printf("%12.8f %12.8f %12.8f\n", row...)
end

# Verification
@printf("\nVerify R*va = [||va||, 0, 0]:\n")
vpa = R * va
@printf("%12.8f %12.8f %12.8f\n", vpa...)

@printf("\nVerify R*vb = [dot(vb,e1), dot(vb,e2), 0]:\n")
vpb = R * vb
@printf("%12.8f %12.8f %12.8f\n", vpb...)

@printf("\nDerived c-axis unit vector e3 = %s\n", string(e3))
