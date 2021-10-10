import lzma
import time

import sys

t = time.time()


f = lzma.open(sys.argv[1], 'rb')
data = f.read()
f.close()

with open(sys.argv[2], 'wb') as f:
    f.write(data)


with open('processing/decompression_time', 'w') as f:
    f.write(str((time.time() - t)*1000))
