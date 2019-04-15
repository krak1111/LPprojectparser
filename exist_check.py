import os
import json
def subdomain_to_list():

    walking_path = os.path.join(os.getcwd(), 'journals')
    for root, _, files in os.walk(walking_path):
        print('root: ', root, '\nfiles: ', files)
        for file in files:
            file_path = os.path.join(os.getcwd(), root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            lines[2] = lines[2].replace(': "', ': ["').replace('",', '"],')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)




if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subdomain_to_list()
    
