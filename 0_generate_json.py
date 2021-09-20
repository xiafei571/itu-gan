import json

import pandas as pd

DATA_ITU_TYPE_3_GENERATED = './data/itu-type3-generated/'

DATA_ITU_TYPE_3 = './data/itu-type3/'

GENERATED_DATA_CSV = './data/generated_data.csv'

JSON_FILE_LIST = "./type3time_processed.txt"

folder_dict = {"p": "physical", "n": "network", "v": "virtual"}
ori_file_count = 500


def get_json_path(coulumn):
    path = coulumn.split("/")
    return path


def get_json_object(file_path):
    with open(file_path) as jsonFile:
        json_object = json.load(jsonFile)
        jsonFile.close()
    return json_object


def write_to_json(file_path, json_data):
    print('write to', file_path)
    with open(file_path, 'wt') as jsonFile:
        json.dump(json_data, jsonFile)
        jsonFile.close()


def change_value(json_object, column, val):
    # print('column:', column)
    path_list = column.split("/")

    new_obj = update_value(json_object, val, path_list, depth=0)

    return new_obj


def update_value(json_object, val, path_list, depth=0):
    if depth == len(path_list):
        json_object = val
        return json_object

    key = path_list[depth]
    # print('key', key)

    if '#' in key:
        temp = key.split("#")
        json_array = json_object[temp[0]]
        for i in range(len(json_array)):
            obj = json_array[i]
            if obj['name'] == temp[1]:
                chdict = obj
                chdict = update_value(chdict, val, path_list, depth + 1)
                json_array[i] = chdict
                json_object[temp[0]] = json_array

    elif isinstance(json_object, list):
        # bugs by arman
        for i in range(len(json_object)):
            if key in json_object[i].keys():
                chdict = json_object[i][key]
                chdict = update_value(chdict, val, path_list, depth + 1)
                json_object[i][key] = chdict
                break
    else:
        # bug fix
        if key == 'computes0':
            key = key[:-1]
        chdict = json_object[key]
        chdict = update_value(chdict, val, path_list, depth + 1)
        json_object[key] = chdict

    return json_object


def get_columns_dict(columns):
    column_dict = {}
    for column in columns:
        file_type = folder_dict[column[0]]
        path_list = column_dict.get(file_type, [])
        path_list.append(column)
        column_dict[file_type] = path_list

    return column_dict


if __name__ == '__main__':
    # init file_list e.g."./type3time_processed.txt"
    f = open(JSON_FILE_LIST, "r")
    file_list = f.readlines()
    # file_list[0][:19]
    f.close()

    # load generator data e.g. './data/generated_data.csv'
    df_generator = pd.read_csv('%s' % GENERATED_DATA_CSV)
    try:
        df_generator = df_generator.drop(columns=['Unnamed: 0'])
    except Exception:
        print('column Unnamed: 0 already deleted')
    print(df_generator.shape)

    column_dict = get_columns_dict(df_generator.columns)
    print(column_dict.keys())

    for idx in range(df_generator.shape[0]):

        curr_idx = idx % ori_file_count
        file_name = file_list[curr_idx]

        for file_type, file_columns in column_dict.items():
            json_object = get_json_object(DATA_ITU_TYPE_3 + file_type + '/' + file_name[:19])

            for column in file_columns:
                json_object = change_value(json_object, column[3:], int(df_generator.iloc[idx][column]))

            write_to_json(DATA_ITU_TYPE_3_GENERATED + file_type + '/' + file_name[:13] + str(idx // ori_file_count) + '.json',
                          json_object)
