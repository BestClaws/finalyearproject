import zstandard as zstd
import time

import sys

t = time.time()


with open(sys.argv[1], 'rb') as f:
    d = zstd.ZstdDecompressor()
    decomp = d.decompress(f.read())
    with open(sys.argv[2], 'wb') as g:
    	g.write(decomp)


secs = 0


with open('data/processing_time', 'r') as f:
    secs = f.read()


with open('data/processing_time', 'w') as f:
    f.write(str(  float(secs) +  (time.time() - t)*1000   ))
