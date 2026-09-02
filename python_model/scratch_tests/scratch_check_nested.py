import numpy as np
from qkd_ldpc_sim import load_parity_check_matrix

rate_1_2 = load_parity_check_matrix("1/2")
rate_2_3 = load_parity_check_matrix("2/3")
rate_3_4 = load_parity_check_matrix("3/4")

print("Checking if 3/4 is nested in 1/2:")
try:
    print(np.array_equal(rate_3_4, rate_1_2[:len(rate_3_4)]))
except Exception as e:
    print(e)
