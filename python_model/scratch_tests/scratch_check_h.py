import numpy as np
from qkd_ldpc_sim import load_parity_check_matrix
from hw_exact_sim import base_matrix, Zc

H = load_parity_check_matrix("1/2")
print("H row 0 indices where value is 1:")
indices = np.where(H[0] == 1)[0]
print(indices)

for idx in indices:
    col = idx // Zc
    z = idx % Zc
    print(f"Col {col}, z {z}")
