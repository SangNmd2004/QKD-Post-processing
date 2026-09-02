# ==============================================================================
# Tcl Script to Run Simulation (Vivado)
# ==============================================================================

puts ">>> Checking Project Status..."
if {[current_project -quiet] eq ""} {
    puts ">>> Opening Project QKD_1..."
    open_project D:/XilinxProjects/QKD_1/QKD_1.xpr
} else {
    puts ">>> Project is already open."
}

puts ">>> Fixing broken project paths..."
puts ">>> Fixing broken project paths..."
remove_files -quiet [get_files -quiet -filter {IS_AVAILABLE == 0}]

set current_dir [pwd]
cd "D:/DownloadD/03. Post-Processing-FPGA-QKD-20260508T062156Z-3-001/03. Post-Processing-FPGA-QKD/qkd_post_processing"

puts ">>> Re-adding all Verilog sources using relative paths..."
set ldpc_files [glob -nocomplain rtl/*.v rtl/ldpc_core/*.v rtl/ldpc_core/*/*.v]
foreach f $ldpc_files { add_files -norecurse $f }

set top_files [glob -nocomplain rtl/top/*.v]
foreach f $top_files { add_files -norecurse $f }

set tb_files [glob -nocomplain tb/*.v]
foreach f $tb_files { add_files -norecurse -fileset sim_1 $f }

puts ">>> Adding RS Decoder VHDL files..."
set rs_vhd_files [glob -nocomplain rtl/rs_core/*.vhd]
foreach f $rs_vhd_files {
    add_files -norecurse $f
    set_property file_type "VHDL 2008" [get_files $f]
}

cd $current_dir

puts ">>> Setting Simulation Top Module..."
set_property top tb_hw_co_design [get_filesets sim_1]


puts ">>> Closing active simulation (if any)..."
close_sim -quiet

puts ">>> Resetting simulation cache to force re-compilation..."
reset_simulation

puts ">>> Launching Simulation..."
launch_simulation

puts ">>> Running Simulation for 2 ms..."
run 2 ms

puts ">>> Simulation Complete! Check the Tcl Console for Testbench output."
