import numpy as np
from scratch_float_bp import base_matrix, Zc

expected = np.array([int(l.strip()) for l in open('data/expected_out.txt').readlines()[:2304]])
syn = np.array([int(l.strip()) for l in open('data/syndrome_in.txt').readlines()[:1152]])

H = np.zeros((1152, 2304), dtype=int)
for r in range(12):
    for c in range(24):
        if base_matrix[r][c] != -1:
            H[r*Zc:(r+1)*Zc, c*Zc:(c+1)*Zc] = np.roll(np.eye(Zc, dtype=int), base_matrix[r][c], axis=1)

cur_syn = np.dot(H, expected) % 2
print('H * expected == syn?', np.array_equal(cur_syn, syn))
