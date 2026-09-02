import os, sys, pandas as pd, numpy as np
import io
from contextlib import redirect_stdout
sys.path.append('qkd_post_processing/python_model')
from qkd_ldpc_sim import load_parity_check_matrix, quantize_llr
from hw_exact_sim import simulate

N = 2304
csv_file = 'bb84_key_test_Sim_20260618_002028.csv'
df = pd.read_csv(csv_file)
alice_bits = ''
bob_bits = ''
for index, row in df.iterrows():
    if index < 20: continue
    alice_bits += str(row['key_alice'])
    bob_bits += str(row['key_bob'])
    if len(alice_bits) >= N * 5: break

alice_arr = np.array([int(b) for b in alice_bits[:N*5]])
bob_arr = np.array([int(b) for b in bob_bits[:N*5]])
H = load_parity_check_matrix(rate='1/2')

for mag in [1.0, 1.25, 1.5, 1.75, 2.0]:
    alice_blk = alice_arr[N*4:N*5]
    bob_blk = bob_arr[N*4:N*5]
    llr = np.zeros(N)
    for i in range(N): llr[i] = mag if bob_blk[i] == 0 else -mag
    llr_q = quantize_llr(llr, w=6, frac=2)
    syn = np.dot(H, alice_blk) % 2
    syn_padded = np.pad(syn, (0, 1152 - len(syn)), 'constant') if len(syn) < 1152 else syn[:1152]
    
    with open('qkd_post_processing/data/llr_in.txt', 'w') as f:
        for val in llr_q: f.write(format(val & 0x3F, '06b') + '\n')
    with open('qkd_post_processing/data/syndrome_in.txt', 'w') as f:
        for val in syn_padded: f.write(str(val) + '\n')
    with open('qkd_post_processing/data/expected_out.txt', 'w') as f:
        for val in alice_blk: f.write(str(val) + '\n')
        
    f_out = io.StringIO()
    with redirect_stdout(f_out):
        mismatches = simulate()
    print(f'Mag {mag}: Mismatches = {mismatches}')
