# ==============================================================================
# ULTIMATE VIVADO TCL SCRIPT FOR LDPC FPGA SYNTHESIS & BITSTREAM
# ==============================================================================
# Script này được tối ưu hóa cực đoan để vắt kiệt hiệu năng phần cứng FPGA,
# tự động dò tìm số luồng CPU, ép xung (timing), và xuất báo cáo tự động.

# 1. Tự động lấy số luồng CPU (Max Threads) để tăng tốc độ Build
set max_threads [exec wmic cpu get NumberOfLogicalProcessors | findstr /R "[0-9]"]
set max_threads [string trim $max_threads]
if {$max_threads eq ""} { set max_threads 8 } ;# Fallback
puts ">>> INFO: Tự động phát hiện CPU: Sử dụng $max_threads luồng để Build."
set_param general.maxThreads $max_threads

# 2. Mở Project
set proj_path "D:/XilinxProjects/QKD_1/QKD_1.xpr"
puts ">>> INFO: Đang mở dự án: $proj_path"
if {[current_project -quiet] eq ""} {
    open_project $proj_path
}

# ==============================================================================
# PHẦN 1: TỔNG HỢP (SYNTHESIS) - Tối ưu hóa Area & Retiming
# ==============================================================================
puts ">>> PHASE 1: Bắt đầu quá trình Synthesis..."
reset_run synth_1

# Chiến lược: Flow_PerfOptimized_high (Bật tính năng Retiming để dịch chuyển Register, tăng Fmax)
set_property strategy Flow_PerfOptimized_high [get_runs synth_1]
set_property STEPS.SYNTH_DESIGN.ARGS.RETIMING true [get_runs synth_1]

launch_runs synth_1 -jobs $max_threads
wait_on_run synth_1

if {[get_property PROGRESS [get_runs synth_1]] != "100%"} {
    puts ">>> ERROR: Synthesis thất bại. Vui lòng kiểm tra mã RTL."
    exit 1
}

# ==============================================================================
# PHẦN 2: TRIỂN KHAI (IMPLEMENTATION) - Ép Timing cực độ
# ==============================================================================
puts ">>> PHASE 2: Bắt đầu quá trình Implementation..."
reset_run impl_1

# Chiến lược: Performance_ExtraTimingOpt (Vivado sẽ chạy nhiều thuật toán hơn để fix Setup/Hold time)
set_property strategy Performance_ExtraTimingOpt [get_runs impl_1]

# Kích hoạt Physical Optimization nâng cao (Post-Route)
set_property STEPS.PHYS_OPT_DESIGN.IS_ENABLED true [get_runs impl_1]
set_property STEPS.POST_ROUTE_PHYS_OPT_DESIGN.IS_ENABLED true [get_runs impl_1]

launch_runs impl_1 -jobs $max_threads
wait_on_run impl_1

if {[get_property PROGRESS [get_runs impl_1]] != "100%"} {
    puts ">>> ERROR: Implementation thất bại. Kiểm tra vấn đề Tắc nghẽn mạch (Routing Congestion)."
    exit 1
}

# ==============================================================================
# PHẦN 3: XUẤT BÁO CÁO (REPORTING) - Tự động hóa tài liệu luận văn
# ==============================================================================
puts ">>> PHASE 3: Đang xuất báo cáo tự động (Timing, Utilization, Power)..."
open_run impl_1

set report_dir "D:/DownloadD/03. Post-Processing-FPGA-QKD-20260508T062156Z-3-001/03. Post-Processing-FPGA-QKD/qkd_post_processing/reports"
file mkdir $report_dir

report_timing_summary -file $report_dir/timing_summary.rpt
report_utilization -file $report_dir/utilization.rpt
report_power -file $report_dir/power.rpt

puts ">>> INFO: Đã lưu báo cáo tại: $report_dir"

# ==============================================================================
# PHẦN 4: XUẤT BITSTREAM
# ==============================================================================
puts ">>> PHASE 4: Đang biên dịch file Bitstream (.bit)..."
launch_runs impl_1 -to_step write_bitstream -jobs $max_threads
wait_on_run impl_1

if {[get_property PROGRESS [get_runs impl_1]] != "100%"} {
    puts ">>> ERROR: Quá trình sinh Bitstream thất bại!"
    exit 1
}

puts ">>> ========================================================================"
puts ">>> SUCCESS: XUẤT XẮC! HỆ THỐNG ĐÃ ĐƯỢC TỔNG HỢP VÀ SINH BITSTREAM THÀNH CÔNG!"
puts ">>> ========================================================================"
exit 0
