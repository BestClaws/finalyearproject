import os
import math




file_names = ['a','b', 'c','d','e', 'f', 'g', 'h', 'i', 'j']
extension = '.txt'
path = 'txt/'


files = []
for file_name in file_names:
	files.append(file_name + extension)



# start looping files here
for file in files:
	print(os.path.join(path, file))

	#original size
	original_size = str(os.stat(os.path.join(path, file)).st_size/1000)
	print(original_size)

	# compression
	command = "python333 src/zstd/compress.py" + "  " +  os.path.join(path,file) + " " + os.path.join('processing', file+"_compressed")
	os.system(command)


	# compression time
	compression_time = None

	with open('processing/compression_time', 'r') as f:
		compression_time = f.read()

	print(compression_time)

	# compressed size
	compressed_size = str(os.stat(os.path.join('processing', file+"_compressed")).st_size/1000)
	print(compressed_size)

	# decompression

	command = "python333 src/zstd/decompress.py" + "  " +  os.path.join('processing', file+"_compressed") + " " + os.path.join('processing', file+"_compressed_decompressed")
	os.system(command)

	#decompression time
	decompression_time = None

	with open('processing/decompression_time', 'r') as f:
		decompression_time = f.read()

	print(decompression_time)

	# decompressed size

	decompressed_size = str(os.stat(os.path.join('processing', file+"_compressed_decompressed")).st_size/1000)
	print(decompressed_size)




	# encryption


	command = "python333 src/aes/aes.py --key-file src/aes/aes.priv --encrypt" + "  " +  os.path.join(path, file) + " " + os.path.join('processing', file+"_encrypted")
	os.system(command)


	# encryption time

	encryption_time = None

	with open('processing/encryption_time', 'r') as f:
		encryption_time = f.read()

	print(encryption_time)

	# encrypted size

	encrypte_size = None

	encrypted_size = str(os.stat(os.path.join('processing', file+"_encrypted")).st_size/1000)
	print(encrypted_size)

	# decryption

	command = "python333 src/aes/aes.py --key-file src/aes/aes.priv --decrypt" + "  " +  os.path.join('processing', file+"_encrypted") + " " + os.path.join('processing', file+"_encrypted_decrypted")
	os.system(command)

	# decryption time

	decryption_time = None

	with open('processing/decryption_time', 'r') as f:
		decryption_time = f.read()

	print(decryption_time)

	# decrypted size


	decrypte_size = None

	decrypted_size = str(os.stat(os.path.join('processing', file+"_encrypted_decrypted")).st_size/1000)
	print(decrypted_size)


	# compression and encryption

	# compressed and encrypted time


	compression_and_encryption_time = None

	semi_compression_time = compression_time
	semi_encryption_time = None

	command = "python333 src/aes/aes.py --key-file src/aes/aes.priv --encrypt" + "  " +  os.path.join('processing', file+"_compressed") + " " + os.path.join('processing', file+"_compressed_encrypted")
	os.system(command)



	with open('processing/encryption_time', 'r') as f:
		semi_encryption_time = f.read()

	compression_and_encryption_time = str(float(semi_compression_time) + float(semi_encryption_time))

	print(compression_and_encryption_time)

	# compressed and encrypted size

	compressed_and_encrypted_size = str(os.stat(os.path.join('processing', file+"_compressed_encrypted")).st_size/1000)
	print(compressed_and_encrypted_size)


	# decryption and decompression

	# decryption and decompression  time

	decryption_and_decompression_time = None

	semi_decompression_time = decompression_time
	semi_decryption_time = None

	command = "python333 src/aes/aes.py --key-file src/aes/aes.priv --decrypt" + "  " +  os.path.join('processing', file+"_compressed_encrypted") + " " + os.path.join('processing', file+"_compressed_encrypted_decrypted")
	os.system(command)



	with open('processing/decryption_time', 'r') as f:
		semi_decryption_time = f.read()

	decryption_and_decompression_time = str(float(semi_decryption_time) +  float(semi_decompression_time))

	print(decryption_and_decompression_time)


	# decompression and decryption size

	decrypted_and_decompressed_size = str(os.stat(os.path.join(path, file)).st_size/1000)
	print(original_size)

	with open(os.path.join('processing', 'stats.csv'), 'a') as f:
		data = original_size + "," + compression_time + "," + decompression_time + "," + compressed_size + "," + decompressed_size + "," + encryption_time + "," + decryption_time + "," + encrypted_size + "," + decrypted_size + "," + compression_and_encryption_time + "," + decryption_and_decompression_time + "," + compressed_and_encrypted_size + "," + decrypted_and_decompressed_size + "\n"
		f.write(data)