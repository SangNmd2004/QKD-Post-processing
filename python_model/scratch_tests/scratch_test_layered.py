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

alice_blk = np.array([int(b) for b in alice_bits[N:N*2]])
bob_blk = np.array([int(b) for b in bob_bits[N:N*2]])

H_12 = load_parity_check_matrix(rate='1/2')
syn_12 = np.dot(H_12, alice_blk) % 2
H_34 = H_12[:576, :]
syn_34 = syn_12[:576]

llr = np.array([1.75 if b == 0 else -1.75 for b in bob_blk])
L = np.round(llr * 4).astype(int)

offset = 2

M, N_cols = H_34.shape
C2V = np.zeros((H_12.shape[0], N_cols), dtype=int)

for it in range(32):
    for i in range(M):
        connected_vns = np.where(H_34[i, :] == 1)[0]
        
        # Calculate V2C from current LLRs
        V2C_curr = np.zeros(len(connected_vns), dtype=int)
        for idx, j in enumerate(connected_vns):
            V2C_curr[idx] = L[j] - C2V[i, j]
            
        C2V_new = np.zeros(len(connected_vns), dtype=int)
        for idx, j in enumerate(connected_vns):
            min_val = 999
            sgn = 1
            for k_idx, k in enumerate(connected_vns):
                if k != j:
                    val = V2C_curr[k_idx]
                    min_val = min(min_val, abs(val))
                    sgn *= np.sign(val) if val != 0 else 1
            if syn_34[i] == 1: sgn = -sgn
            val_offset = min_val - offset if min_val > offset else 0
            C2V_new[idx] = sgn * val_offset
            
        for idx, j in enumerate(connected_vns):
            C2V[i, j] = C2V_new[idx]
            L[j] = V2C_curr[idx] + C2V_new[idx]
            L[j] = np.clip(L[j], -64, 63)
            
    decoded = np.where(L > 0, 0, 1)
    errs = np.sum(decoded != alice_blk)
    if errs == 0:
        print(f"Converged at iter {it}")
        break

print(f"Errors = {errs}")
