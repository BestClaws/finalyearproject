import sys
import os
import json

import requests

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, asymmetric
from cryptography.hazmat.primitives.asymmetric import padding



with open('data/server_address') as f:
    server_address = f.read()


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
		priv_key = serialization.load_ssh_private_key(
			key_txt,
			password=None,
			backend=default_backend())
	else:
		return ValueError('key value not present')
	return priv_key





def main():


    user_name = sys.argv[1]
    target_user = sys.argv[2]
    package_name = sys.argv[3]
    
    with open('data/processing/send_temp') as f:
        info = json.load(f)


    tu_pub_key = create_pub_key(bytes(info['tu_public_key'], 'utf-8'))
    enc_package_key = bytes(info['enc_package_key']) 


    with open('data/key', 'rb') as f:
        priv_key = create_priv_key(f.read())



    package_key = dec(enc_package_key,priv_key)

    new_enc_package_key = enc(package_key, tu_pub_key)
	

    response = {
        "user_name": user_name,
        "target_user": target_user,
        "package_name": package_name,
        "new_enc_package_key": list(new_enc_package_key)
    }

    r = requests.post(server_address + '/send_package?', json=response)

    if r.ok == True:
        print('all done')
    else:
        print('all not done')

main()
