import lzma

import sys




f = lzma.open(sys.argv[1], 'rb')
data = f.read()
f.close()

with open(sys.argv[2], 'wb') as f:
    f.write(data)

