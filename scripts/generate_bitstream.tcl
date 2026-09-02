# ==============================================================================
# Tcl Script for Optimal Bitstream Generation (Vivado)
# ==============================================================================

puts ">>> Checking Project Status..."
if {[current_project -quiet] eq ""} {
    puts ">>> Opening Project QKD_1..."
    open_project D:/XilinxProjects/QKD_1/QKD_1.xpr
} else {
    puts ">>> Project is already open."
}

# ------------------------------------------------------------------------------
# 1. Synthesis Phase (Optimized for Performance)
# ------------------------------------------------------------------------------
puts ">>> Configuring Synthesis for High Performance..."
reset_run synth_1

# Thiết lập chiến lược Synthesis ưu tiên tối ưu hóa hiệu suất (Fmax cao)
set_property strategy Flow_PerfOptimized_high [get_runs synth_1]
# Bạn cũng có thể dùng Flow_AreaOptimized_high nếu bị thiếu tài nguyên LUT/FF
# set_property strategy Flow_AreaOptimized_high [get_runs synth_1]

puts ">>> Launching Synthesis (Sử dụng tối đa luồng CPU)..."
# Tùy chỉnh -jobs bằng số luồng CPU máy bạn có (ví dụ 8 hoặc 16)
launch_runs synth_1 -jobs 8
wait_on_run synth_1

# Kiểm tra xem Synthesis có thành công không
if {[get_property PROGRESS [get_runs synth_1]] != "100%"} {
    puts ">>> [ERROR] Synthesis failed! Vui lòng kiểm tra log."
    exit 1
}

# ------------------------------------------------------------------------------
# 2. Implementation Phase (Optimized for Routing & Timing)
# ------------------------------------------------------------------------------
puts ">>> Configuring Implementation for Explore Strategy..."
reset_run impl_1

# Thiết lập chiến lược Implementation: Performance_Explore
# Chiến lược này cho phép Vivado vét cạn các thuật toán tối ưu Timing và Routing. Rất tốt cho lõi LDPC phức tạp.
set_property strategy Performance_Explore [get_runs impl_1]

puts ">>> Launching Implementation..."
launch_runs impl_1 -jobs 8
wait_on_run impl_1

if {[get_property PROGRESS [get_runs impl_1]] != "100%"} {
    puts ">>> [ERROR] Implementation failed! Vui lòng kiểm tra Timing hoặc Routing congestion."
    exit 1
}

# ------------------------------------------------------------------------------
# 3. Bitstream Generation
# ------------------------------------------------------------------------------
puts ">>> Launching Bitstream Generation..."
launch_runs impl_1 -to_step write_bitstream -jobs 8
wait_on_run impl_1

if {[get_property PROGRESS [get_runs impl_1]] != "100%"} {
    puts ">>> [ERROR] Bitstream Generation failed!"
    exit 1
}

puts ">>> ========================================================================"
puts ">>> [SUCCESS] TỔNG HỢP VÀ XUẤT BITSTREAM THÀNH CÔNG!"
puts ">>> File .bit của bạn đã sẵn sàng tại thư mục: D:/XilinxProjects/QKD_1/QKD_1.runs/impl_1/"
puts ">>> ========================================================================"

exit 0
