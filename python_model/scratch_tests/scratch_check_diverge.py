import numpy as np
import sys

with open("python_model/hw_exact_sim.py", "r") as f:
    code = f.read()

code = code.replace("C2V_MAX = (1 << (res_w - 1)) - 1    # 127", "C2V_MAX = 31")
code = code.replace("C2V_MIN = -(1 << (res_w - 1))       # -128", "C2V_MIN = -32")

with open("python_model/hw_exact_sim_dbg2.py", "w") as f:
    f.write(code)

import hw_exact_sim_dbg2
hw_exact_sim_dbg2.simulate()
