import os
import secrets
import time

print('started')

while True:



    try:


        os.system("aws s3 cp s3://s3-worm/slave2/status data/status")        

        with open('data/status') as f:
            status = f.read()
            status  = status.strip('\n')
            # print('read status:', status)
    except FileNotFoundError:
        # print('status file not found')
        status = 'STOP'

   
    if status == 'START':

        os.system("rm -rf data/")
        os.system("aws s3 sync s3://s3-worm/slave2/ data/ --delete")

        # print('working')
        os.system("echo '0' >  data/processing_time")

        processing_time = 0.0
        compressed_size = 0.0
        package_key = ""

        with open('data/package_key') as f:
            package_key = f.read()

        
        # print('status set to start')

        # print('got list of files from data/input')
        # get a list of files
        try:
            files_all = os.listdir('data/input')
        except FileNotFoundError:
            print('not task assigned.. doing nothing')

           # print('settings status to stop')
            with open('data/status', 'w') as f:
                f.write('STOP')

            os.system("aws s3 sync data/ s3://s3-worm/slave2/ --delete")

            continue
            		
        files = []

        for ef in files_all:

            if ef.endswith('.enc'):
                os.unlink('data/input/' + ef)
            else:
                files.append(ef)

        print('list of files to process:', files)    
    
        for ef in files:

            print('compressing file:', ef)
            os.system("python3 stages/zstd/compress.py" + " " + "data/input/" + ef + " " + "data/input/" + ef + ".comp")
            # print('deleting original file: data/input/', ef)
            # os.system("rm data/input/" + ef)
            os.system("mv data/input/" + ef  + " ./original" )
            compressed_size += os.stat("data/input/" + ef + ".comp").st_size
            # print('\tcumulative compressed size:', compressed_size)

        



        for ef in files:

            print('encrypting file:', ef, 'with package key:', package_key)
            os.system("python3 stages/aes/aes.py --key " + package_key + " --encrypt data/input/" + ef + ".comp data/input/" + ef + ".enc")
            os.system("rm data/input/" + ef + ".comp")
  



        # print('settings status to stop')
        with open('data/status', 'w') as f:
            f.write('STOP')

        os.system("aws s3 sync data/ s3://s3-worm/slave2/ --delete")

    else:
        # print('status not START so doing nothing')
        time.sleep(1)
        print('..')
        continue

