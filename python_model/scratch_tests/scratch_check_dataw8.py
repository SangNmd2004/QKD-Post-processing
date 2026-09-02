import sys

with open("python_model/hw_exact_sim.py", "r") as f:
    code = f.read()

code = code.replace("data_w = 6      # LLR width", "data_w = 8")
code = code.replace("MAX_ITER = 5", "MAX_ITER = 50")
code = code.replace("MAX_ITER = 1", "MAX_ITER = 50") # In case it was 1
code = code.replace("C2V_MAX = 31", "C2V_MAX = 127")
code = code.replace("C2V_MIN = -32", "C2V_MIN = -128")

with open("python_model/hw_exact_sim_dbg6.py", "w") as f:
    f.write(code)

import hw_exact_sim_dbg6
hw_exact_sim_dbg6.simulate()
