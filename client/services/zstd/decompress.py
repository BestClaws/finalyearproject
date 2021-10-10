import zstandard as zstd


import sys


with open(sys.argv[1], 'rb') as f:
    d = zstd.ZstdDecompressor()
    decomp = d.decompress(f.read())
    with open(sys.argv[2], 'wb') as g:
    	g.write(decomp)


