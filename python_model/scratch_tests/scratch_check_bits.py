import numpy as np
from qkd_ldpc_sim import load_parity_check_matrix
from hw_exact_sim import load_test_data, base_matrix, Zc

llrs, syndrome, expected = load_test_data()
H = load_parity_check_matrix("1/2")

print("Checking Layer 0, z=7")
layer = 0
z = 7

# Bits from H matrix
h_indices = np.where(H[layer * Zc + z] == 1)[0]
h_bits = [expected[idx] for idx in h_indices]

# Bits from v2c_shifted
v2c_bits = []
for col in range(24):
    shift_val = base_matrix[layer][col]
    if shift_val != -1:
        idx = col * Zc + (z + shift_val) % Zc
        v2c_bits.append(expected[idx])

print(f"H indices: {h_indices}")
print(f"H bits:    {h_bits}")
print(f"v2c bits:  {v2c_bits}")

print(f"H sum mod 2:   {sum(h_bits) % 2}")
print(f"v2c XOR sum: {np.bitwise_xor.reduce(v2c_bits)}")
