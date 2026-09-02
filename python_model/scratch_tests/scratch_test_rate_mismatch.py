import os, sys, numpy as np
import io
from contextlib import redirect_stdout
sys.path.append('qkd_post_processing/python_model')
from qkd_ldpc_sim import load_parity_check_matrix, quantize_llr
from hw_exact_sim import simulate
import pandas as pd

N = 2304
csv_file = 'bb84_key_test_Sim_20260618_002028.csv'
df = pd.read_csv(csv_file)
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
syn_padded = np.pad(syn_12, (0, 1152 - len(syn_12)), 'constant') if len(syn_12) < 1152 else syn_12[:1152]

llr = np.zeros(N)
for i in range(N): llr[i] = 1.75 if bob_blk[i] == 0 else -1.75
llr_q = quantize_llr(llr, w=6, frac=2)

with open('qkd_post_processing/data/llr_in.txt', 'w') as f:
    for val in llr_q: f.write(format(val & 0x3F, '06b') + '\n')
with open('qkd_post_processing/data/syndrome_in.txt', 'w') as f:
    for val in syn_padded: f.write(str(val) + '\n')
with open('qkd_post_processing/data/expected_out.txt', 'w') as f:
    for val in alice_blk: f.write(str(val) + '\n')

print("Simulating Block 1 with Rate 1/2 Syndrome, but decoding at Rate 3/4...")
f_out = io.StringIO()
with redirect_stdout(f_out):
    mismatches = simulate(rate='3/4', max_iter=32)
print(f"Mismatches after Rate 3/4: {mismatches}")

print("Simulating Block 1 with Rate 1/2 Syndrome, decoding at Rate 1/2...")
f_out = io.StringIO()
with redirect_stdout(f_out):
    mismatches = simulate(rate='1/2', max_iter=32)
print(f"Mismatches after Rate 1/2: {mismatches}")
