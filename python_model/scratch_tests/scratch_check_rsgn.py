import numpy as np
import os
import sys

with open("python_model/hw_exact_sim.py", "r") as f:
    code = f.read()

code = code.replace("parity_vector[z] = rsgn", "parity_vector[z] = rsgn\n                if rsgn != 0:\n                    print(f'Layer {layer} z {z} rsgn=1! syn={syn_2d[layer][z]}')")
code = code.replace("MAX_ITER = 100", "MAX_ITER = 1")

with open("python_model/hw_exact_sim_dbg.py", "w") as f:
    f.write(code)

import hw_exact_sim_dbg
hw_exact_sim_dbg.simulate()
