import sys
import requests
import time

package_path =  sys.argv[3]
url =  sys.argv[4]


headers = {
	'user_name': sys.argv[1],
	'package_name': sys.argv[2]
}

with open(package_path, 'rb') as f:
	res = requests.post(url, data=f, headers=headers)

print(res)