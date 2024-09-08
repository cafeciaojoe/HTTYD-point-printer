import json
import csv
import os

"""Converts the .json files made in httyd to cvs to be usedin blendplot"""

def return_path_to_csv(json_file_path):
    directory = os.path.dirname(json_file_path)
    file_name_with_extension = os.path.basename(json_file_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    file_name_with_csv_extension = file_name + '.csv'
    csv_path = os.path.join(directory, file_name_with_csv_extension)
    return csv_path

def load_accepted_positions(json_file_path):
    #     https://stackoverflow.com/questions/36965507/writing-a-dictionary-to-a-text-file

    with open(json_file_path, 'r') as f:
        accepted_positions = json.loads(f.read())
        print('loaded %d position from save file' % (len(accepted_positions.keys())))
        'print(accepted_positions.keys())'
        'print(accepted_positions.items()'
    return accepted_positions

def create_csv(json_file_path):

    coord_dict = load_accepted_positions(json_file_path)

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

    path_to_csv = return_path_to_csv(json_file_path)

    with open(path_to_csv, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(axes)

        for i in range(len(x)):
            row = [x[i],y[i],z[i]]
            writer.writerow(row)

        print('plotted %d points to csv' % len(x))

    return path_to_csv
