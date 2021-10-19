import pandas as pd

# 2_csv_combine 3_csv_combine 4_train_diff
# TRAIN_PATH: ./dataset/csv-for-learning/
# TEST_PATH: ./dataset/csv-for-evaluation/
# CSV_DATA_SET: ./csv/dataset.csv
# CSV_TEST_SET: ./csv/testset.csv
# CSV_DIFF_DATA_SET: ./csv/diff_dataset.csv
# CSV_DIFF_TEST_SET: ./csv/diff_testset.csv


dataset_path = './data/generated_all_data.csv'
diff_dataset_path = './csv/all/diff_dataset_type11_3.csv'


def get_diff_dataset(dataset, X_train, type=0):
    diff_dataset = pd.DataFrame(columns=dataset.columns)
    cur_type = type # useless, can delete
    start_index = 0

    for index, row in dataset.iterrows():

        if index == 0:
            pass

        row_type = row[-1]

        if (index + 1) % 5 == 0:
            end_index = index
            diff_df = X_train.loc[[start_index, end_index]].diff().loc[[end_index]]
            diff_df['v_type_code'] = cur_type
            diff_dataset = diff_dataset.append(diff_df, ignore_index=True, sort=False)
            # new start
            start_index = index + 1
            cur_type = row_type

    diff_dataset['v_type_code'] = pd.to_numeric(diff_dataset['v_type_code'])
    return diff_dataset


def main():
    print('reading dataset...')
    dataset = pd.read_csv(dataset_path)
    # delete zero columns
    dataset = dataset.loc[:, (dataset != 0).any(axis=0)]
    print('dataset', dataset.shape)
    # Segmentation training tests
    column = dataset.columns
    X_train = dataset[column[:-2]]
    y_train = dataset[column[-1]]

    print('get diff dataset...')
    diff_dataset = get_diff_dataset(dataset, X_train, type=3)

    # Remove the useless fields.
    diff_dataset.drop(['v_type'], axis=1, inplace=True)
    # Remove the effect of time on results.
    diff_dataset.drop(['p_/time'], axis=1, inplace=True)
    diff_dataset.drop(['v_/time'], axis=1, inplace=True)
    # Delete the first two unknown columns (doesn't work~)
    # diff_dataset.drop(columns=['Unnamed: 0'], inplace=True)
    # diff_testset.drop(columns=['Unnamed: 0'], inplace=True)

    print('writing to csv..')
    diff_dataset.to_csv(diff_dataset_path, index=False)
    print('diff_dataset:', diff_dataset.shape)


if __name__ == '__main__':
    main()
