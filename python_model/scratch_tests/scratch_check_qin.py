import numpy as np
from hw_exact_sim import load_test_data, base_matrix, barrel_shift, NUM_COLS, D_cnu, Zc, MAX_POS_VAL

llrs, syndrome, expected = load_test_data()

layer = 0
z = 7
connected_cols = []
for col in range(NUM_COLS):
    if base_matrix[layer][col] != -1:
        connected_cols.append((col, base_matrix[layer][col]))

q_in_buffer = np.full((D_cnu, Zc), MAX_POS_VAL, dtype=int)

for degree_idx, (col, shift_val) in enumerate(connected_cols):
    if degree_idx >= D_cnu: break
    llr_block = llrs[col*Zc:(col+1)*Zc]
    v2c_shifted = barrel_shift(llr_block, shift_val)
    q_in_buffer[degree_idx] = v2c_shifted

q_in_D = [q_in_buffer[d][z] for d in range(D_cnu)]
print(f"q_in_D for layer 0 z 7: {q_in_D}")
qsgn = [1 if val < 0 else 0 for val in q_in_D]
print(f"qsgn: {qsgn}")
print(f"qsgn_sum: {np.bitwise_xor.reduce(qsgn)}")
