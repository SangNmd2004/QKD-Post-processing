# ==============================================================================
# Tcl Script: build_optimized_bitstream.tcl
# Mục đích: Biên dịch hệ thống giải mã LDPC QKD với cấu hình tối ưu nhất cho Vivado
# Hướng dẫn chạy: Trên giao diện Vivado, gõ lệnh dưới đây vào Tcl Console:
# source {d:/DownloadD/03. Post-Processing-FPGA-QKD-20260508T062156Z-3-001/03. Post-Processing-FPGA-QKD/qkd_post_processing/scripts/build_optimized_bitstream.tcl}
# ==============================================================================

# 0. Tối ưu số luồng CPU (Giúp biên dịch nhanh hơn)
set_param general.maxThreads 8

# Mở Project (Giả sử bạn đang lưu ở đường dẫn này theo log lỗi trước đó của bạn)
set proj_path "D:/XilinxProjects/QKD_1/QKD_1.xpr"

if {[current_project -quiet] == ""} {
    if {[file exists $proj_path]} {
        open_project $proj_path
        puts "\[INFO\] Opened Project: $proj_path"
    } else {
        puts "\[WARNING\] Không tìm thấy Project ở $proj_path. Vui lòng mở Project thủ công trước khi chạy lệnh."
    }
} else {
    puts "\[INFO\] Project hiện tại đã được mở sẵn: [current_project]"
}

# ==========================================
# 1. TỐI ƯU HÓA TỔNG HỢP (SYNTHESIS)
# ==========================================
puts "\[INFO\] Đang cấu hình Tối ưu Tổng hợp (Synthesis)..."
reset_run synth_1

# Hệ thống LDPC (Partially Parallel) có mạng lưới nối dây khổng lồ giữa VNU và CNU.
# - FLATTEN_HIERARCHY: rebuilt -> Gỡ bỏ ranh giới các module con để tối ưu hóa logic chéo.
# - RETIMING: true -> Tự động dịch chuyển các thanh ghi (D Flip-Flops) qua lại giữa các 
#   khối logic để giảm Delay path, tăng tần số tối đa (Fmax) - Cực kỳ quan trọng cho vòng lặp LDPC!
set_property STEPS.SYNTH_DESIGN.ARGS.FLATTEN_HIERARCHY rebuilt [get_runs synth_1]
set_property STEPS.SYNTH_DESIGN.ARGS.RETIMING true [get_runs synth_1]

# Launch Synthesis
puts "\[INFO\] Bắt đầu chạy Synthesis..."
launch_runs synth_1 -jobs 8
wait_on_run synth_1

# ==========================================
# 2. TỐI ƯU HÓA SẮP XẾP VÀ ĐI DÂY (IMPLEMENTATION)
# ==========================================
puts "\[INFO\] Đang cấu hình Tối ưu Đi dây (Implementation)..."
reset_run impl_1

# Kiến trúc LDPC thường chết ở khâu đi dây do nghẽn cổ chai (Congestion) tại Barrel Shifter.
# Sử dụng chiến thuật AltRouting và AggressiveExplore để ép Vivado dồn sức giải quyết nghẽn mạng.
set_property STEPS.OPT_DESIGN.ARGS.DIRECTIVE Explore [get_runs impl_1]
set_property STEPS.PLACE_DESIGN.ARGS.DIRECTIVE AltRouting [get_runs impl_1]
set_property STEPS.PHYS_OPT_DESIGN.IS_ENABLED true [get_runs impl_1]
set_property STEPS.PHYS_OPT_DESIGN.ARGS.DIRECTIVE AggressiveExplore [get_runs impl_1]
set_property STEPS.ROUTE_DESIGN.ARGS.DIRECTIVE AggressiveExplore [get_runs impl_1]

# Launch Implementation
puts "\[INFO\] Bắt đầu chạy Implementation (Quá trình này có thể mất nhiều thời gian)..."
launch_runs impl_1 -jobs 8
wait_on_run impl_1

# ==========================================
# 3. XUẤT BITSTREAM
# ==========================================
# Ép nén Bitstream để giảm kích thước file, giúp Zynq PS nạp mã PL nhanh hơn
set_property STEPS.WRITE_BITSTREAM.ARGS.READBACK_FILE 0 [get_runs impl_1]
set_property STEPS.WRITE_BITSTREAM.ARGS.VERBOSE 0 [get_runs impl_1]
# Cài đặt thuộc tính nén trực tiếp vào Thiết kế (Design)
open_run impl_1
set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]

puts "\[INFO\] Bắt đầu xuất file Bitstream..."
launch_runs impl_1 -to_step write_bitstream -jobs 8
wait_on_run impl_1

puts "=================================================="
puts "SUCCESS! Đã đóng gói thành công Bitstream tối ưu."
puts "Hãy kiểm tra Timing Report (WNS) để xem hệ thống đã đạt Timing Closure chưa nhé!"
puts "=================================================="
