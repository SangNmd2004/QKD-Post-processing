import sys
import numpy as np

with open("python_model/hw_exact_sim.py", "r") as f:
    code = f.read()

# Make sure MAX_ITER is large enough
code = code.replace("MAX_ITER = 5", "MAX_ITER = 50")

# And we keep the C2V bounds small to prevent v2c sign flip as proven earlier
code = code.replace("C2V_MAX = (1 << (res_w - 1)) - 1    # 127", "C2V_MAX = 31")
code = code.replace("C2V_MIN = -(1 << (res_w - 1))       # -128", "C2V_MIN = -32")

with open("python_model/hw_exact_sim_dbg5.py", "w") as f:
    f.write(code)

import hw_exact_sim_dbg5
from hw_exact_sim_dbg5 import load_test_data

original_load = hw_exact_sim_dbg5.load_test_data
def modified_load():
    llrs, syn, exp = original_load()
    # Boost magnitude: 7 -> 18, -7 -> -18
    new_llrs = np.where(llrs > 0, 18, -18)
    return new_llrs, syn, exp

hw_exact_sim_dbg5.load_test_data = modified_load
hw_exact_sim_dbg5.simulate()
