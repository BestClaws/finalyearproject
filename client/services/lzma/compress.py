import lzma
import sys


with open(sys.argv[1], 'rb') as f:
    data = f.read()



f = lzma.open(sys.argv[2], 'wb')
f.write(data)
f.close()



