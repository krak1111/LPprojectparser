import subprocess


def main():
    while True:
       
        p = subprocess.Popen('python parsermain.py', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        (_, err) = p.communicate()
        if 'ConnectionError' in str(err):
            print('Reboot script')
        print(err)




if __name__ == '__main__':
    main()