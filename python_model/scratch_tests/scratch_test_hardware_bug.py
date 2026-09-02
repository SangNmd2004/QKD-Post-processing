import sys, numpy as np
sys.path.append('qkd_post_processing/python_model')
from qkd_ldpc_sim import load_parity_check_matrix, quantize_llr
import pandas as pd

N = 2304
df = pd.read_csv('bb84_key_test_Sim_20260618_002028.csv')
alice_bits = ''
bob_bits = ''
for index, row in df.iterrows():
    if index < 20: continue
    alice_bits += str(row['key_alice'])
    bob_bits += str(row['key_bob'])
    if len(alice_bits) >= N * 2: break

# Block 1
alice_blk = np.array([int(b) for b in alice_bits[N:N*2]])
bob_blk = np.array([int(b) for b in bob_bits[N:N*2]])

H_12 = load_parity_check_matrix(rate='1/2')
H_34 = load_parity_check_matrix(rate='3/4')

syn_12 = np.dot(H_12, alice_blk) % 2
# Hardware uses first 576 bits of syn_12 as Rate 3/4 syndrome
syn_hw = syn_12[:576]

# Let's run a simple Min-Sum decoder mimicking hardware
llr = np.array([1.75 if b == 0 else -1.75 for b in bob_blk])
# Scale by 4 (frac=2)
L = np.round(llr * 4).astype(int)

# Decoder logic
M, N_cols = H_34.shape
V2C = np.zeros((M, N_cols), dtype=int)
C2V = np.zeros((M, N_cols), dtype=int)

for i in range(M):
    for j in range(N_cols):
        if H_34[i, j] == 1:
            V2C[i, j] = L[j]

MAX_ITER = 32
for it in range(MAX_ITER):
    # Check node update
    for i in range(M):
        connected_vns = np.where(H_34[i, :] == 1)[0]
        for j in connected_vns:
            # Min-sum
            min_val = 999
            sgn = 1
            for k in connected_vns:
                if k != j:
                    val = V2C[i, k]
                    min_val = min(min_val, abs(val))
                    sgn *= np.sign(val) if val != 0 else 1
            # Apply syndrome
            if syn_hw[i] == 1:
                sgn = -sgn
            C2V[i, j] = sgn * min_val
            
    # Variable node update
    L_new = L.copy()
    for j in range(N_cols):
        connected_cns = np.where(H_34[:, j] == 1)[0]
        sum_c2v = np.sum(C2V[connected_cns, j])
        L_new[j] = L[j] + sum_c2v
        
        # Update V2C
        for i in connected_cns:
            V2C[i, j] = L_new[j] - C2V[i, j]
            
    # Hard decision
    decoded = np.where(L_new > 0, 0, 1)
    errs = np.sum(decoded != alice_blk)
    if it == 0 or it == 31:
        print(f"Iter {it}: mismatches with Alice = {errs}")

