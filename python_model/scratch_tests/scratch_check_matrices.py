import sys, numpy as np
sys.path.append('qkd_post_processing/python_model')
from qkd_ldpc_sim import load_parity_check_matrix

H_12 = load_parity_check_matrix(rate='1/2')
H_34 = load_parity_check_matrix(rate='3/4')

print(f"H_12 shape: {H_12.shape}")
print(f"H_34 shape: {H_34.shape}")

# Check if the top 576 rows of H_12 are EXACTLY equal to H_34
are_equal = np.array_equal(H_12[:576, :], H_34)
print(f"Are the first 576 rows of Rate 1/2 identical to Rate 3/4? {are_equal}")
