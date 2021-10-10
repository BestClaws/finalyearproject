import sys
import os
import sys
import time
import json
import copy
import time
import secrets


from flask import Flask, request, jsonify
from werkzeug.datastructures import FileStorage



from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, asymmetric
from cryptography.hazmat.primitives.asymmetric import padding


app = Flask(__name__, static_url_path='/dl', static_folder='../dl')
val = None

@app.route('/upload_package', methods=['GET', 'POST'])
def upload_package():

    if request.method == 'POST':
        
        package_name = request.headers['package_name']
        user_name = request.headers['user_name']

        print('request from user: ', user_name, ' to upload package: ', package_name)

        # clean the processing folder
        os.system("rm -rf data/processing/*")

        print('saving received package...')
        FileStorage(request.stream).save(os.path.join('data', 'processing',package_name))
        print('unpacking package archive...')
        os.system('unzip data/processing/' + package_name + ' -d data/processing/')
        print('getting rid of archive now...')
        os.system('rm data/processing/' + package_name)
        print('getting files list...')
        files = os.listdir('data/processing')
        print('listing files: ')
        for ef in files:
            print('file: ', ef)
        

        files_duo = []
        original_size = 0
        compressed_size = 0
        processing_time = 0.0


        package_key = secrets.token_urlsafe(24)
        print('generated package key: ', package_key)

        for ef in files:

            print("processing file:  ", ef)
            original_size += os.stat("data/processing/" + ef).st_size
            print('\tfile size: ', original_size)
            fh = secrets.token_urlsafe(6)
            files_duo.append({'file_name': ef, 'file_hash': fh})
            print('\trenaming file to:', fh)
            os.system("mv data/processing/" + ef + " " + "data/processing/" + fh)
            
        for ef in files_duo:

            print('compressing file:', ef['file_name'])
            os.system("python3 stages/zstd/compress.py" + " " + "data/processing/" + ef['file_hash'] + " " + "data/processing/" + ef['file_hash'] + ".comp")
            compressed_size += os.stat("data/processing/" + ef['file_hash'] + ".comp").st_size
            print('\tcumulative compressed size:', compressed_size)
            with open('data/processing/compression_time', 'r') as f:
                processing_time += float(f.read())
        



        for ef in files_duo:

            print('encrypting file:', ef['file_name'])

            os.system("python3 stages/aes/aes.py --key " + package_key + " --encrypt data/processing/" + ef['file_hash'] + ".comp data/processing/" + ef['file_hash'] + ".enc")

            with open('data/processing/encryption_time', 'r') as f:
                processing_time += float(f.read())


        for ef in files_duo:
            print("moving file: ", ef['file_name'], " to data/files/")
            os.system("mv data/processing/" + ef['file_hash'] + ".enc data/files/" + ef['file_hash'] + ".enc")
            
        print('updating database...')
        with open('data/users.json') as f:
            users = json.load(f)


        user_pub_key = create_pub_key(bytes(users[user_name]['public_key'], 'utf-8'))
        
        print(type(user_pub_key))
        print(user_pub_key)
        enc_package_key = list(enc(bytes(package_key, 'utf-8'), user_pub_key))



        users[user_name]['packages'].append({
            "package_name" : package_name,
            "package_owner": user_name,
            "enc_package_key" : enc_package_key,
            "files_list" : files_duo,
            "original_size" : original_size/ 1024,
            "compressed_size" : compressed_size / 1024,
            "processing_time": processing_time
        })

        with open('data/users.json', 'w') as f:
            json.dump(users, f, indent=2)




        return 'okay', 200
        
    return 'working'




@app.route('/list_packages', methods=['GET'])
def list_packages():
    user_name = request.args['user_name']
    with open('data/users.json') as f:
        users = json.load(f)
    return jsonify(users[user_name]['packages']), 200



@app.route('/delete_package', methods=['GET'])
def delete_package():
    
    user_name = request.args['user_name']
    package_name = request.args['package_name']

    with open('data/users.json') as f:
        users = json.load(f)
    
    packages = users[user_name]['packages']

    ind = None

    for i, package in enumerate(packages):
        if(package['package_name'] == package_name):
            ind = i
            break

    del(packages[ind])

    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=2)

    return 'deleted'





@app.route('/download_package', methods=['GET'])
def download_package():
    print(request.args)
    user_name = request.args['user_name']
    package_name = request.args['package_name']
    with open('data/users.json') as f:
        users = json.load(f)
    
    packages = users[user_name]['packages']

    ind = None

    for i, package in enumerate(packages):
        if(package['package_name'] == package_name):
            ind = i
            break

    files_list = packages[ind]['files_list']


    # restore original names
    os.system("rm -rf data/processing/*") # clean processing folder
    
    for ef in files_list:
        os.system("cp data/files/" + ef['file_hash'] + ".enc data/processing/" + ef['file_name'] + ".enc")

    print(os.listdir("data/processing/"))

    files_list_str = " "

    for ef in files_list:
        files_list_str +=   "data/processing/" + ef['file_name'] + ".enc "


    package_key = bytes(packages[ind]['enc_package_key'])

    with open('data/processing/key', 'wb') as f:
        f.write(package_key)


    files_list_str += 'data/processing/key' # include package key along with files

    print(files_list_str)


    os.system("zip -j data/processing/package_" + package_name + "_by_" + user_name + ".zip " + files_list_str)
    os.system("mv data/processing/package_" + package_name + "_by_" + user_name + ".zip " + " dl/" )

    os.system("rm -rf data/processing/*") # clean processing folder

    return 'link generated'





@app.route('/send_package', methods=['GET', 'POST'])
def send_package():



    # retreive user info
    with open('data/users.json') as f:
        users = json.load(f)


    if request.method == 'POST':

        data = request.json

        user_name = data["user_name"]
        target_user = data["target_user"]
        package_name = data["package_name"]
        new_enc_package_key = data["new_enc_package_key"]

        print(user_name, target_user, package_name)




        # owning user and target user's packages
        tu_packages = users[target_user]['packages']
        packages = users[user_name]['packages']


        ind = None
        for i, package in enumerate(packages):
            if(package['package_name'] == package_name):
                ind = i
                break



        # grab the target package from owner
        package_info = copy.deepcopy(packages[ind])
        package_info['enc_package_key'] = new_enc_package_key


        tu_packages.append(package_info)

        users[target_user]['packages'] = tu_packages

        with open('data/users.json', 'w') as f:
            json.dump(users, f, indent=2)

        
        return 'OK'


    if request.method == 'GET':





        user_name = request.args['user_name']
        package_name = request.args['package_name']
        target_user = request.args['target_user']

        # owning user and target user's packages
        tu_packages = users[target_user]['packages']
        packages = users[user_name]['packages']

        print(user_name, package_name, target_user)

        ind = None
        for i, package in enumerate(packages):
            if(package['package_name'] == package_name):
                ind = i
                break

        # grab the target user's public key
        tu_public_key = users[target_user]['public_key']

        # grab the encrypted, package's key 
        enc_package_key = packages[ind]['enc_package_key']

        res = { 
            "tu_public_key": tu_public_key,
            "enc_package_key": enc_package_key
        }

        return jsonify(res)




@app.route('/create_user',  methods=['GET','POST'])
def create_user():

    if request.method == 'GET':
        return 'yes'

    data = request.json

    user_name = data['user_name']
    pub_key = data['pub_key']

    with open('data/users.json') as f:
        users = json.load(f)
    


    users[user_name] = {"public_key": pub_key, "packages": []}


    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=2)
    
    return jsonify({"user": "created"}), 200



def enc(message, pub_key):
	"""encrypt the message using the public key"""
	
	
	
	cipher_txt = pub_key.encrypt(
		message,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None))

	return cipher_txt




def create_pub_key(key_txt=None):
	"""serializes a public key object from given key"""
	if key_txt is not None:
		pub_key = serialization.load_ssh_public_key(
			key_txt,
			default_backend())
	else:
		return ValueError('key value not present')
	return pub_key




# run the server
app.run(debug=True)




# extra methods



