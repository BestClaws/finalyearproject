import huffman
import time
import sys

file_name = sys.argv[1]
out_file = sys.argv[2]
code_book = None



time1 = time.time()


with open(file_name, 'rb') as stream:
    read_file = stream.read()


frequency = huffman.calculate_frequency(read_file)



encoding, code_book = huffman.create_encoding(frequency, read_file)
huffman.write_binary_encoding(encoding, out_file)
huffman.write_code_book(code_book, 'code_book')

time2 = time.time()

with open('processing/compression_time', 'w') as f:
    f.write(str((time2 - time1)*1000))





