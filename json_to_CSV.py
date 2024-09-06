import json
import csv
import os

def return_with_csv_extension(file_path):
    file_name_with_extension = os.path.basename(file_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    return file_name + '.csv'

def load_accepted_positions(file_path):
    #     https://stackoverflow.com/questions/36965507/writing-a-dictionary-to-a-text-file

    with open(file_path, 'r') as f:
        accepted_positions = json.loads(f.read())
        print('loaded %d position from save file' % (len(accepted_positions.keys())))
        'print(accepted_positions.keys())'
        'print(accepted_positions.items()'
    return accepted_positions

def create_csv(file_path):

    coord_dict = load_accepted_positions(file_path)

    "x's are 0 and 3"
    "y's are 1 and 4"
    "z's are 2 and 5"

    axes = ['x','y','z']
    x=[]
    y=[]
    z=[]

    for key, value in coord_dict.items():
        x.append(value[0])
        y.append(value[1])
        z.append(value[2])
        x.append(value[3])
        y.append(value[4])
        z.append(value[5])

    "length of each list is 2x78 = 156"
    "print(len(x))"

    path_to_csv = 'working_files/' + return_with_csv_extension(file_path)

    with open(path_to_csv, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(axes)

        for i in range(len(x)):
            row = [x[i],y[i],z[i]]
            writer.writerow(row)

        print('plotted %d points to csv' % len(x))

    return path_to_csv
