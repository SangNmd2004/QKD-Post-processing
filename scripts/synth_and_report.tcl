# Vivado Synthesis and Reporting Script
# Run this script in Vivado Tcl Console: source d:/DownloadD/03. Post-Processing-FPGA-QKD-20260508T062156Z-3-001/03. Post-Processing-FPGA-QKD/qkd_post_processing/scripts/synth_and_report.tcl

set proj_name "QKD_CoDesign_Sim"
set top_module "system_top"

puts "========================================================="
puts " STARTING SYNTHESIS & TIMING CLOSURE (TARGET: 150 MHz) "
puts "========================================================="

# Create a virtual clock constraint of 150MHz (6.666 ns)
set constraint_file "timing_constraints.xdc"
set fileId [open $constraint_file "w"]
puts $fileId "create_clock -period 6.666 -name clk -waveform {0.000 3.333} \[get_ports clk\]"
close $fileId

add_files -fileset constrs_1 -norecurse $constraint_file
set_property target_constrs_file $constraint_file [current_fileset -constrset]

# Run Synthesis
reset_run synth_1
launch_runs synth_1 -jobs 8
wait_on_run synth_1

# Open Synthesized Design
open_run synth_1 -name synth_1

puts "========================================================="
puts " EXTRACTING REPORTS... "
puts "========================================================="

# Generate Timing Report
report_timing_summary -file timing_summary_150MHz.rpt -delay_type min_max -report_unconstrained -check_timing_verbose -max_paths 10 -nworst 1 -significant_digits 3 -name timing_1

# Generate Power Report
report_power -file power_summary.rpt -name power_1

# Generate Utilization (Resource) Report
report_utilization -file utilization_summary.rpt -name utilization_1

puts "========================================================="
puts " TIMING CLOSURE & BENCHMARKING COMPLETE! "
puts " Reports saved to the project directory: "
puts " 1. timing_summary_150MHz.rpt "
puts " 2. power_summary.rpt "
puts " 3. utilization_summary.rpt "
puts "========================================================="
