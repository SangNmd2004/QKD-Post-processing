# QKD Post-Processing on FPGA (Gowin)

This repository contains the RTL (Verilog/VHDL) source code for a Hardware-Algorithm Co-Design of a QKD Post-Processing pipeline (LDPC + Reed-Solomon), optimized for Gowin FPGAs (e.g., Gowin 138K Pro).

## Repository Structure

- `rtl/`: Contains the synthesizable Verilog and VHDL source files.
  - `ldpc_core/`: The Partially Parallel LDPC Decoder core.
  - `rs_core/`: The Reed-Solomon (255, 223) Outer Code decoder.
  - `top/`: Top-level integration and wrappers (`system_top.v`, etc.).
- `tb/`: Testbench files (`tb_hw_co_design.v`, `tb_system_top.v`) for Vivado simulation.
- `python_model/`: Python scripts for generating test vectors and verifying the algorithm.
- `scripts/`: TCL scripts for synthesis and bitstream generation.

## How to add this project to Gowin EDA

To synthesize and implement this design on a Gowin FPGA, follow these steps:

### 1. Create a New Gowin Project
1. Open **Gowin IDE**.
2. Go to **File** -> **New** -> **FPGA Design Project**.
3. Name your project (e.g., `QKD_Post_Processing`) and select your target device (e.g., `GW5AST-138B`).

### 2. Add the Source Files
1. In the **Design** tab (usually on the left panel), right-click on the project name and select **Add Files**.
2. Navigate to the cloned repository and add all `.v` and `.vhd` files from the following directories:
   - `rtl/`
   - `rtl/ldpc_core/`
   - `rtl/rs_core/`
   - `rtl/top/`
3. **Set the Top Module:** Right-click on `system_top.v` in the Design tree and select **Set as Top Module**. This ensures Gowin synthesizes the entire pipeline correctly without trying to compile sub-modules independently.

### 3. Configure Synthesis Strategy (Crucial for BRAM Limits)
Because the Reed-Solomon core and LDPC parity matrices are large, you may encounter `Out of memory` errors during default synthesis in Gowin. You must optimize for Area and disable RAM inference for certain modules:
1. Right-click on your project name -> **Configuration**.
2. Go to **Synthesize** -> **General**.
3. Change **Synthesis Strategy** to **Area**.
4. Check the box for **Disable RAM Inference** (forces Gowin to use LUTs instead of failing to allocate BRAMs if the matrix is too irregular).
5. (Optional) If you have the Gowin EDA version that includes **Synplify Pro**, go to `Synthesize Tool` and select `Synplify Pro` for much better optimization.

### 4. Run the Flow
- Double-click **Synthesize** in the Process pane.
- Once synthesis passes, configure your pin constraints (CST file) if you plan to program the board.
- Double-click **Place & Route** (PnR).
- Double-click **Generate Bitstream**.

## Simulation using Vivado
Because Gowin's built-in simulator can be slow with large VHDL generics, we recommend using Vivado for Behavioral Simulation:
1. Generate test vectors by running: `python python_model/batch_run_sim.py`
2. Add all `rtl/` and `tb/` files to a Vivado project.
3. Run the **Behavioral Simulation** on `tb_hw_co_design.v`.
4. The testbench will automatically iterate through 5 QBER noise levels (2% to 6%) and output a summary report table showing the Syndrome Hamming Weight (SHW) and remaining errors.
