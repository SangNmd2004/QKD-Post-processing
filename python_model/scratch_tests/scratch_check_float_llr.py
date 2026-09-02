import numpy as np
import os
from scratch_float_bp import load_data, base_matrix, Zc, M, N

llrs_old, syn, expected = load_data()

# Reconstruct bob_key from llrs_old
bob_key = np.where(llrs_old > 0, 0, 1)

# Compute new LLRs for 1% QBER (LLR ~ 4.6)
llrs = np.where(bob_key == 0, 4.6, -4.6)

# Build Graph
H = np.zeros((M, N), dtype=int)
for r in range(12):
    for c in range(24):
        shift = base_matrix[r][c]
        if shift != -1:
            I = np.eye(Zc, dtype=int)
            I_shifted = np.roll(I, shift, axis=1)
            H[r*Zc:(r+1)*Zc, c*Zc:(c+1)*Zc] = I_shifted

# Float Min-Sum BP
R_mn = np.zeros((M, N))
L_n = np.copy(llrs)

for it in range(50):
    parity_ok = True
    for m in range(M):
        connected_n = np.where(H[m] == 1)[0]
        v2c = L_n[connected_n] - R_mn[m, connected_n]
        
        for idx, n in enumerate(connected_n):
            others = np.delete(v2c, idx)
            sgn = np.prod(np.sign(others)) * (-1 if syn[m] == 1 else 1)
            mag = np.min(np.abs(others))
            # Offset Min-Sum with offset 0.5
            mag = max(0, mag - 0.5)
            R_mn[m, n] = sgn * mag
            
    L_n = llrs + np.sum(R_mn, axis=0)
    
    decoded = (L_n < 0).astype(int)
    current_syn = np.dot(H, decoded) % 2
    if np.array_equal(current_syn, syn):
        print(f"Converged at iter {it}")
        break

errors = np.sum(decoded != expected)
print(f"Float BP errors: {errors}")
