import os
def load_bits(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

llr_lines = load_bits('qkd_post_processing/data/llr_in.txt')
exp_lines = load_bits('qkd_post_processing/data/expected_out.txt')

for b in range(6):
    llr_blk = llr_lines[b*2304 : (b+1)*2304]
    exp_blk = exp_lines[b*2304 : (b+1)*2304]
    errs = 0
    for i in range(2304):
        sign = '1' if llr_blk[i].startswith('1') else '0' # Wait, 6-bit 2's complement. Negative is '1'
        if sign != exp_blk[i]:
            errs += 1
    print(f"Block {b} LLR sign mismatches vs expected: {errs}")
