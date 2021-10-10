import sys
import os
import requests

package_name = sys.argv[1]

os.system("rm -rf data/processing/*")

with open('data/server_address') as f:
    server_address = f.read()



r = requests.get( server_address + '/dl/' + package_name)

with open('data/processing/' + package_name,'wb') as f:
    f.write(r.content)

os.system('unzip data/processing/' + package_name + ' -d data/processing/')
os.system('rm data/processing/' + package_name)


os.system("python3 services/rsa/rsa.py --key-file data/key --decrypt data/processing/key data/processing/package_key")

package_key = ""
with open('data/processing/package_key') as f:
    package_key = f.read()



os.system('rm data/processing/key data/processing/package_key')



# grab list of files in package
files = os.listdir('data/processing/')


# decrypt and decompress each file.
for ef in files:
    actual_name = ef.split('.enc')[0]

    os.system('python3 services/aes/aes.py --key ' + package_key + ' --decrypt data/processing/' + ef + ' data/processing/' + actual_name + '.dec')
    os.system('python3 services/zstd/decompress.py   data/processing/' + actual_name + '.dec data/processing/' + actual_name)
    os.system('rm data/processing/' + ef + ' data/processing/' + actual_name + '.dec')
os.system("caja data/processing/")

print(package_key)
print('done')
