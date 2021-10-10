# encrypt.py

# built-in modules
import sys
import os

# third party modules
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend




def grab_params():

    key_txt = None

    if '--key' in sys.argv:
        
        offset = sys.argv.index('--key')
        key_txt = sys.argv[offset + 1]
    
    elif '--key-file' in sys.argv:

        offset = sys.argv.index('--key-file')
        file_src = sys.argv[offset + 1]

        with open(file_src) as f:
            key_txt = f.read()

    # key in bytes, in contrast to text
    key = bytes(key_txt,'utf-8')


    # grab the file info and operation to be performed
    task = None   

    if '--encrypt' in sys.argv:
        task = 'encrypt'
        offset = sys.argv.index('--encrypt')

    elif '--decrypt' in sys.argv:
        task = 'decrypt'
        offset = sys.argv.index('--decrypt')     
        
    in_file_src = sys.argv[offset+1]
    out_file_src = sys.argv[offset+2]

    return (key, task, in_file_src, out_file_src)



def main():

    # resources
    key = ''
    encryptor = None
    decryptor = None
    old_buffer = None
    cipher_backend = default_backend()
    # end of resources

    
 
    # grab the file and operation to be done
    key, task, in_file_src, out_file_src = grab_params()



    # create a cipher (secretive way to encode message)
    cipher = Cipher(algorithms.AES(key), # use the AES algorithm implementation with our key
        modes.OFB(key[0:16]), # use the Cipher Block Chain mode (one of many available modes)
        backend=cipher_backend) #  the cipher maker class to use

    # grab the encryptors and decryptors from cipher class
    encryptor = cipher.encryptor()
    decryptor = cipher.decryptor()


    # read the source file
    with open(in_file_src, 'rb') as f:
        old_buffer = f.read()

    # determine the task and encrypt or decrypt accordingly
    if task == 'encrypt':
        new_buffer  = encryptor.update(old_buffer) + encryptor.finalize()
    elif task == 'decrypt':
        new_buffer = decryptor.update(old_buffer) + decryptor.finalize()
 
    # write to target file
    with open(out_file_src, 'wb') as f:
        f.write(new_buffer)
    


if __name__ == '__main__':
    main()
