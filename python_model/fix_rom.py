import os
rom_path = 'qkd_post_processing/rtl/ir_qc_ldpc/matlinsas_LDPC/rom_h_matrix.v'
with open(rom_path, 'r') as f:
    lines = f.readlines()

out_lines = []
for i in range(21):
    out_lines.append(lines[i])

# Append Rate 1/2 rows directly
out_lines.append("        // Unconditionally use Rate 1/2 Matrix for Rate-Compatible Blind Reconciliation\n")
out_lines.append("        // Rate 3/4 uses top 6 rows. Rate 2/3 uses top 8 rows. Rate 1/2 uses 12 rows.\n")

rate_1_2_start = 22 # "case (row_idx)"
rate_1_2_end = 141 # "endcase"

for i in range(rate_1_2_start, rate_1_2_end + 1):
    # reduce indent by 4 spaces
    line = lines[i]
    if line.startswith("    "):
        line = line[4:]
    out_lines.append(line)

out_lines.append("    end\n")
out_lines.append("endmodule\n")

with open(rom_path, 'w') as f:
    f.writelines(out_lines)
