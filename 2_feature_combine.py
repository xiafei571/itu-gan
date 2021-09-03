import pandas as pd

# 2_csv_combine 3_csv_combine 4_train_diff
# TRAIN_PATH: ./dataset/csv-for-learning/
# TEST_PATH: ./dataset/csv-for-evaluation/
# CSV_DATA_SET: ./csv/dataset.csv
# CSV_TEST_SET: ./csv/testset.csv
# CSV_DIFF_DATA_SET: ./csv/diff_dataset.csv
# CSV_DIFF_TEST_SET: ./csv/diff_testset.csv


train_path = './dataset/csv-for-learning/gan4/'
dataset_path = './csv/dataset.csv'


# Combining three types of csv.
def df_combine(train_n_files, train_v_files, train_p_files):
    li_n = []
    li_v = []
    li_p = []
    li_test_n = []
    li_test_v = []
    li_test_p = []
    # train
    for filename in train_n_files:
        print('read_csv network:', filename)
        df = pd.read_csv(filename, index_col=None, header=0)
        li_n.append(df)
    for filename in train_v_files:
        print('read_csv virtual:', filename)
        df = pd.read_csv(filename, index_col=None, header=0)
        li_v.append(df)
    for filename in train_p_files:
        print('read_csv physical:', filename)
        df = pd.read_csv(filename, index_col=None, header=0)
        li_p.append(df)

    dataset_n = pd.concat(li_n, axis=0, ignore_index=True, sort=False)
    dataset_v = pd.concat(li_v, axis=0, ignore_index=True, sort=False)
    dataset_p = pd.concat(li_p, axis=0, ignore_index=True, sort=False)

    print('dataset_n_v_p:')
    print(dataset_n.shape)
    print(dataset_v.shape)
    print(dataset_p.shape)

    dataset_p.drop(['type', 'type_code'], axis=1, inplace=True)
    dataset_n.drop(['type', 'type_code'], axis=1, inplace=True)

    dataset_n.rename(columns=lambda x: 'n_' + x, inplace=True)
    dataset_v.rename(columns=lambda x: 'v_' + x, inplace=True)
    dataset_v['common_time_index'] = dataset_v['v_/time']
    dataset_p.rename(columns=lambda x: 'p_' + x, inplace=True)
    dataset_p['common_time_index'] = dataset_p['p_/time']

    # dataset = pd.concat([dataset_n, dataset_v, dataset_p], axis=1, sort=False)
    dataset_pn = pd.merge(dataset_p, dataset_n, how='inner', left_index=True, right_index=True)
    dataset = pd.merge(dataset_pn, dataset_v, how='inner', on=['common_time_index'])

    # Delete the temporary fields used to join the table
    dataset.drop(['common_time_index'], axis=1, inplace=True)

    # Delete lines with outliers
    dataset.dropna(axis=0, how='any', inplace=True)
    return dataset


def main():
    # train_n_files = glob.glob(train_path + "*.n.csv")
    # train_v_files = glob.glob(train_path + "*.v.csv")
    # test_n_files = glob.glob(train_path + "*.p.csv")
    # test_n_files = glob.glob(test_path + "*.n.csv")
    # test_v_files = glob.glob(test_path + "*.v.csv")
    # test_p_files = glob.glob(test_path + "*.p.csv")

    train_n_files = [train_path + x for x in
                     ['20200629.n.csv', '20200630.n.csv', '20200702.n.csv', '20200703.n.csv',
                      '20200704.n.csv',]]
    train_v_files = [train_path + x for x in
                     ['20200629.v.csv', '20200630.v.csv', '20200702.v.csv', '20200703.v.csv',
                      '20200704.v.csv']]
    train_p_files = [train_path + x for x in
                     ['20200629.p.csv', '20200630.p.csv', '20200702.p.csv', '20200703.p.csv',
                      '20200704.p.csv']]


    dataset = df_combine(train_n_files, train_v_files, train_p_files)
    print('save to csv..')
    dataset.to_csv(dataset_path)
    print('dataset:')
    print(dataset.shape)


if __name__ == '__main__':
    main()
