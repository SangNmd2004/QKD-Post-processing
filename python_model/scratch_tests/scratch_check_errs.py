import numpy as np
from hw_exact_sim import load_test_data, base_matrix, barrel_shift, NUM_COLS, D_cnu, Zc, MAX_POS_VAL

llrs, syndrome, expected = load_test_data()

layer = 0
z = 0
connected_cols = []
for col in range(NUM_COLS):
    if base_matrix[layer][col] != -1:
        connected_cols.append((col, base_matrix[layer][col]))

q_in_buffer = np.full((D_cnu, Zc), MAX_POS_VAL, dtype=int)
qsgn_expected = []
expected_vals = []
indices = [190, 265, 823, 947, 1159, 1248]
for idx in indices:
    expected_vals.append(expected[idx])

for degree_idx, (col, shift_val) in enumerate(connected_cols):
    if degree_idx >= D_cnu: break
    llr_block = llrs[col*Zc:(col+1)*Zc]
    v2c_shifted = barrel_shift(llr_block, shift_val)
    q_in_buffer[degree_idx] = v2c_shifted
    qsgn_expected.append(1 if v2c_shifted[z] < 0 else 0)

print(f"Expected values at indices: {expected_vals}")
print(f"qsgn expected: {qsgn_expected}")
qsgn_sum = np.bitwise_xor.reduce(qsgn_expected)
expected_sum = np.bitwise_xor.reduce(expected_vals)
print(f"expected_sum = {expected_sum}, qsgn_sum = {qsgn_sum}, syn_bit = {syndrome[0]}")
