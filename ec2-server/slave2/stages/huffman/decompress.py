import huffman
import time
import sys

file_name = sys.argv[1]
out_file = sys.argv[2]


time1 = time.time()


decoded_file = huffman.decode_file('code_book', file_name)

with open(out_file, 'wb') as stream:
    stream.write(bytes(decoded_file))


time2 = time.time()

with open('processing/decompression_time', 'w') as f:
    f.write(str((time2 - time1)*1000))
