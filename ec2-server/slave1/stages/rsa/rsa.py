import sys
import os


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, asymmetric
from cryptography.hazmat.primitives.asymmetric import padding



def grab_params():

    key_txt = None

    
    if '--key-file' in sys.argv:

        offset = sys.argv.index('--key-file')
        file_src = sys.argv[offset + 1]

        with open(file_src, 'rb') as f:
            key_txt = f.read()


    task = None   

    if '--encrypt' in sys.argv:
        task = 'encrypt'
        offset = sys.argv.index('--encrypt')

    elif '--decrypt' in sys.argv:
        task = 'decrypt'
        offset = sys.argv.index('--decrypt')     
        
    in_file_src = sys.argv[offset+1]
    out_file_src = sys.argv[offset+2]

    return (key_txt, task, in_file_src, out_file_src)



def enc(message, pub_key):
	"""encrypt the message using the public key"""
	
	
	
	cipher_txt = pub_key.encrypt(
		message,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None))

	return cipher_txt


def dec(cipher_txt, priv_key):
	"""decrypts the cipher text using the private key"""
	message = priv_key.decrypt(
		cipher_txt,
		asymmetric.padding.OAEP(
			mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None))

	return message


def create_pub_key(key_txt=None):
	"""serializes a public key object from given key"""
	if key_txt is not None:
		pub_key = serialization.load_ssh_public_key(
			key_txt,
			default_backend())
	else:
		return ValueError('key value not present')
	return pub_key


def create_priv_key(key_txt=None):
	"""serializes a private key object from given key"""
	if key_txt is not None:
		priv_key = serialization.load_pem_private_key(
			key_txt,
			password=None,
			backend=default_backend())
	else:
		return ValueError('key value not present')
	return priv_key





def main():

	key_txt, task, in_file_src, out_file_src = grab_params()



	if task == 'encrypt':

			pub_key = create_pub_key(key_txt)

			with open(in_file_src, 'rb') as fp:
				data = fp.read()

			encoded_data = enc(data, pub_key)
			
			with open(out_file_src, 'wb') as fp:
				fp.write(encoded_data)
	
	elif task == 'decrypt':

			with open(in_file_src, 'rb') as fp:
				encoded_data = fp.read()

			priv_key = create_priv_key(key_txt)
			
			data = dec(encoded_data,priv_key)

			with open(out_file_src, 'wb') as fp:
				fp.write(data)

if __name__ == '__main__':
	main()
