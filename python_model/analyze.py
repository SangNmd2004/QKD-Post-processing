with open('d:/DownloadD/03. Post-Processing-FPGA-QKD-20260508T062156Z-3-001/03. Post-Processing-FPGA-QKD/qkd_post_processing/data/llr_in.txt') as f:
    llrs = [int(x, 2) for x in f.read().split()]
with open('d:/DownloadD/03. Post-Processing-FPGA-QKD-20260508T062156Z-3-001/03. Post-Processing-FPGA-QKD/qkd_post_processing/data/expected_out.txt') as f:
    exp = [int(x, 2) for x in f.read().split()]

print(f'Total LLR samples: {len(llrs)}, Total expected bits: {len(exp)}')
print()

final_errors = [22, 0, 0, 0, 0, 146]
for block in range(6):
    block_llrs = llrs[block*2304 : (block+1)*2304]
    block_exp = exp[block*2304 : (block+1)*2304]
    
    signed_llrs = [x - 64 if x >= 32 else x for x in block_llrs]
    hd = [1 if x < 0 else 0 for x in signed_llrs]
    
    init_err = sum(1 for h, e in zip(hd, block_exp) if h != e)
    qber = init_err / 2304 * 100
    fe = final_errors[block]
    corrected = init_err - fe
    status = 'SUCCESS' if fe == 0 else 'FAILED'
    corr_pct = corrected / init_err * 100 if init_err > 0 else 0
    
    print(f'Block {block}: Init={init_err} errors ({qber:.2f}%), Final={fe}, Corrected={corr_pct:.1f}%, Status={status}')

print()
for block in range(6):
    block_llrs = llrs[block*2304 : (block+1)*2304]
    signed_llrs = [x - 64 if x >= 32 else x for x in block_llrs]
    avg_mag = sum(abs(x) for x in signed_llrs) / len(signed_llrs)
    min_mag = min(abs(x) for x in signed_llrs)
    max_mag = max(abs(x) for x in signed_llrs)
    zeros = sum(1 for x in signed_llrs if x == 0)
    print(f'Block {block}: avg|LLR|={avg_mag:.2f}, min={min_mag}, max={max_mag}, zero_count={zeros}')
