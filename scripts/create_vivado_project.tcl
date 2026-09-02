# ==============================================================================
# Tcl Script to Create/Rebuild Vivado Project
# Run this script in the Vivado Tcl Console:
# source d:/DownloadD/03. Post-Processing-FPGA-QKD-20260508T062156Z-3-001/03. Post-Processing-FPGA-QKD/qkd_post_processing/scripts/create_vivado_project.tcl
# ==============================================================================

set PROJECT_NAME "QKD_LDPC_Sim"
set PROJECT_DIR "d:/DownloadD/03. Post-Processing-FPGA-QKD-20260508T062156Z-3-001/03. Post-Processing-FPGA-QKD/vivado_project"
set SRC_DIR "d:/DownloadD/03. Post-Processing-FPGA-QKD-20260508T062156Z-3-001/03. Post-Processing-FPGA-QKD/qkd_post_processing"

# Close any open project
close_project -quiet

# Create project
puts ">>> Creating new Vivado project..."
create_project -force $PROJECT_NAME $PROJECT_DIR -part xc7z020clg400-1

# Add RTL source files (Exclude archive_legacy)
puts ">>> Adding RTL source files..."
add_files [glob -nocomplain $SRC_DIR/rtl/ldpc_core/*.v]
add_files [glob -nocomplain $SRC_DIR/rtl/ldpc_core/cnu/*.v]
add_files [glob -nocomplain $SRC_DIR/rtl/pa_core/*.v]
add_files [glob -nocomplain $SRC_DIR/rtl/top/*.v]

# Set Top Module
set_property top qkd_post_processing_top [current_fileset]

# Add Testbench files
puts ">>> Adding Testbench files..."
add_files -fileset sim_1 [glob -nocomplain $SRC_DIR/tb/*.v]
set_property top tb_system_top [get_filesets sim_1]

puts ">>> Project created successfully at $PROJECT_DIR!"
puts ">>> You can now click 'Run Simulation'."
