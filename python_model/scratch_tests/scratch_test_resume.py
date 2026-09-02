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

llr = np.array([1.75 if b == 0 else -1.75 for b in bob_blk])
L = np.round(llr * 4).astype(int)

offset = 2

M, N_cols = H_12.shape
C2V = np.zeros((H_12.shape[0], N_cols), dtype=int)

def run_layers(num_iters, layers, current_syn, H_mat):
    global L, C2V
    for it in range(num_iters):
        for layer in range(layers):
            cns_in_layer = range(layer * 96, (layer + 1) * 96)
            L_old = L.copy()
            C2V_new_layer = np.zeros((96, N_cols), dtype=int)
            for idx, i in enumerate(cns_in_layer):
                connected_vns = np.where(H_mat[i, :] == 1)[0]
                V2C_curr = np.zeros(len(connected_vns), dtype=int)
                for v_idx, j in enumerate(connected_vns):
                    V2C_curr[v_idx] = L_old[j] - C2V[i, j]
                for v_idx, j in enumerate(connected_vns):
                    min_val = 999
                    sgn = 1
                    for k_idx, k in enumerate(connected_vns):
                        if k != j:
                            val = V2C_curr[k_idx]
                            min_val = min(min_val, abs(val))
                            sgn *= np.sign(val) if val != 0 else 1
                    if current_syn[i] == 1: sgn = -sgn
                    val_offset = min_val - offset if min_val > offset else 0
                    C2V_new_layer[idx, j] = sgn * val_offset
            for idx, i in enumerate(cns_in_layer):
                connected_vns = np.where(H_mat[i, :] == 1)[0]
                for j in connected_vns:
                    old_c2v = C2V[i, j]
                    new_c2v = C2V_new_layer[idx, j]
                    C2V[i, j] = new_c2v
                    L[j] = L_old[j] - old_c2v + new_c2v
                    L[j] = np.clip(L[j], -64, 63)
        decoded = np.where(L > 0, 0, 1)
        errs = np.sum(decoded != alice_blk)
        if errs == 0:
            print(f"Converged at iter {it}")
            break

run_layers(32, 6, syn_12[:576], H_12[:576,:])
run_layers(32, 8, syn_12[:768], H_12[:768,:])
run_layers(64, 12, syn_12, H_12)
