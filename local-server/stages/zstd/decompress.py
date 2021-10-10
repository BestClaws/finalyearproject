import zstandard as zstd
import time

import sys

t = time.time()


with open(sys.argv[1], 'rb') as f:
    d = zstd.ZstdDecompressor()
    decomp = d.decompress(f.read())
    with open(sys.argv[2], 'wb') as g:
    	g.write(decomp)



with open('processing/decompression_time', 'w') as f:
    f.write(str((time.time() - t)*1000))
