import json
import os


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.getcwd()
    walking_path = os.path.join(base_dir, 'journals')
    for root, _, files in os.walk(walking_path):
        if not files:
            continue
        for file in files:
            file_path = os.path.join(base_dir, root, file)
            print(file_path)
            with open(file_path) as f:
                lines = f.readlines()
            if lines[-3][-2] == ',':
                lines[-3] = lines[-3][:-2] + '\n'
                with open(file_path, 'w') as f:
                    f.writelines(lines)

            with open(file_path) as f:
                json.load(f)