import numpy as np
from hw_exact_sim import load_test_data
from qkd_ldpc_sim import load_parity_check_matrix

llrs, syndrome, expected = load_test_data()
H = load_parity_check_matrix(rate="1/2")
syn_calc = np.dot(H, expected[:2304]) % 2
print("First 10 calculated syn:", syn_calc[:10])
print("First 10 file syndrome :", syndrome[:10])
