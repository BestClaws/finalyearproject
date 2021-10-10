import zstandard as zstd
import time
import sys

t = time.time()

with open(sys.argv[1], 'rb') as f:
    c = zstd.ZstdCompressor()
    comp = c.compress(f.read())
    with open(sys.argv[2], 'wb') as g:
    	g.write(comp)


with open('data/processing/compression_time', 'w') as f:
    f.write(str((time.time() - t)*1000))
