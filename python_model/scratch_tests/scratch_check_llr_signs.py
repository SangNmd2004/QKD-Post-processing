import numpy as np
from hw_exact_sim import load_test_data

llrs, syndrome, expected = load_test_data()

mismatches = 0
for i in range(2304):
    q = 1 if llrs[i] < 0 else 0
    if q != expected[i]:
        print(f"Index {i}: llr {llrs[i]} implies {q}, expected {expected[i]}")
        mismatches += 1

print(f"Total sign mismatches: {mismatches}")
