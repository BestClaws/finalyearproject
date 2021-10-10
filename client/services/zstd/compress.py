import zstandard as zstd

import sys


with open(sys.argv[1], 'rb') as f:
    c = zstd.ZstdCompressor()
    comp = c.compress(f.read())
    with open(sys.argv[2], 'wb') as g:
    	g.write(comp)

