import lzma
import time
import sys

t = time.time()

with open(sys.argv[1], 'rb') as f:
    data = f.read()



f = lzma.open(sys.argv[2], 'wb')
f.write(data)
f.close()




with open('processing/compression_time', 'w') as f:
    f.write(str((time.time() - t)*1000))
