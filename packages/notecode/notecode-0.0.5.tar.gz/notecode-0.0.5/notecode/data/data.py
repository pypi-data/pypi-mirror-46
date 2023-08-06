#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/03/30 12:10
# @Author  : niuliangtao
# @Site    :
# @File    : data.py
# @Software: PyCharm

import pickle
import random
import zipfile

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from .download import download_file

data_root = '/content/tmp/'


def get_adult_data():
    train_path = data_root + "/data/adult.data.txt"
    test_path = data_root + "/data/adult.test.txt"

    download_file(url="https://raw.githubusercontent.com/1007530194/data/master/recommendation/data/adult.data.txt",
                  path=train_path)
    download_file(url="https://raw.githubusercontent.com/1007530194/data/master/recommendation/data/adult.test.txt",
                  path=test_path)

    train_data = pd.read_table(train_path, header=None, delimiter=',')
    test_data = pd.read_table(test_path, header=None, delimiter=',')

    all_columns = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
                   'marital-status', 'occupation', 'relationship', 'race', 'sex',
                   'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'label', 'type']

    continus_columns = ['age', 'fnlwgt', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']
    dummy_columns = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex',
                     'native-country']

    train_data['type'] = 1
    test_data['type'] = 2

    all_data = pd.concat([train_data, test_data], axis=0)
    all_data.columns = all_columns

    all_data = pd.get_dummies(all_data, columns=dummy_columns)

    test_data = all_data[all_data['type'] == 2].drop(['type'], axis=1)
    train_data = all_data[all_data['type'] == 1].drop(['type'], axis=1)

    train_data['label'] = train_data['label'].map(lambda x: 1 if x.strip() == '>50K' else 0)
    test_data['label'] = test_data['label'].map(lambda x: 1 if x.strip() == '>50K.' else 0)

    for col in continus_columns:
        ss = StandardScaler()
        train_data[col] = ss.fit_transform(train_data[[col]].astype(np.float64))
        test_data[col] = ss.transform(test_data[[col]].astype(np.float64))

    train_y = train_data['label']
    train_x = train_data.drop(['label'], axis=1)
    test_y = test_data['label']
    test_x = test_data.drop(['label'], axis=1)

    return train_x, train_y, test_x, test_y


def get_electronics_data():
    path_root = data_root + "/data/electronics/"

    path1 = path_root + "/reviews_Electronics_5.json.gz"
    path2 = path_root + "/meta_Electronics.json.gz"

    download_file(url="http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Electronics_5.json.gz",
                  path=path1)

    download_file(url="http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/meta_Electronics.json.gz",
                  path=path2)

    f = zipfile.ZipFile(path1, 'r')
    for file in f.namelist():
        f.extract(file, path_root)

    f = zipfile.ZipFile(path2, 'r')
    for file in f.namelist():
        f.extract(file, path_root)

    def convert_pd():

        def to_df(file_path):
            with open(file_path, 'r') as fin:
                df = {}
                i = 0
                for line in fin:
                    df[i] = eval(line)
                    i += 1
                df = pd.DataFrame.from_dict(df, orient='index')
                return df

        reviews_df = to_df('../raw_data/reviews_Electronics_5.json')
        with open('../raw_data/reviews.pkl', 'wb') as f:
            pickle.dump(reviews_df, f, pickle.HIGHEST_PROTOCOL)

        meta_df = to_df('../raw_data/meta_Electronics.json')
        meta_df = meta_df[meta_df['asin'].isin(reviews_df['asin'].unique())]
        meta_df = meta_df.reset_index(drop=True)
        with open('../raw_data/meta.pkl', 'wb') as f:
            pickle.dump(meta_df, f, pickle.HIGHEST_PROTOCOL)

    def remap_id():
        random.seed(1234)

        with open('../raw_data/reviews.pkl', 'rb') as f:
            reviews_df = pickle.load(f)
            reviews_df = reviews_df[['reviewerID', 'asin', 'unixReviewTime']]
        with open('../raw_data/meta.pkl', 'rb') as f:
            meta_df = pickle.load(f)
            meta_df = meta_df[['asin', 'categories']]
            meta_df['categories'] = meta_df['categories'].map(lambda x: x[-1][-1])

        def build_map(df, col_name):
            key = sorted(df[col_name].unique().tolist())
            m = dict(zip(key, range(len(key))))
            df[col_name] = df[col_name].map(lambda x: m[x])
            return m, key

        asin_map, asin_key = build_map(meta_df, 'asin')
        cate_map, cate_key = build_map(meta_df, 'categories')
        revi_map, revi_key = build_map(reviews_df, 'reviewerID')

        user_count, item_count, cate_count, example_count = \
            len(revi_map), len(asin_map), len(cate_map), reviews_df.shape[0]
        print('user_count: %d\titem_count: %d\tcate_count: %d\texample_count: %d' %
              (user_count, item_count, cate_count, example_count))

        meta_df = meta_df.sort_values('asin')
        meta_df = meta_df.reset_index(drop=True)
        reviews_df['asin'] = reviews_df['asin'].map(lambda x: asin_map[x])
        reviews_df = reviews_df.sort_values(['reviewerID', 'unixReviewTime'])
        reviews_df = reviews_df.reset_index(drop=True)
        reviews_df = reviews_df[['reviewerID', 'asin', 'unixReviewTime']]

        cate_list = [meta_df['categories'][i] for i in range(len(asin_map))]
        cate_list = np.array(cate_list, dtype=np.int32)

        with open('../raw_data/remap.pkl', 'wb') as f:
            pickle.dump(reviews_df, f, pickle.HIGHEST_PROTOCOL)  # uid, iid
            pickle.dump(cate_list, f, pickle.HIGHEST_PROTOCOL)  # cid of iid line
            pickle.dump((user_count, item_count, cate_count, example_count),
                        f, pickle.HIGHEST_PROTOCOL)
            pickle.dump((asin_key, cate_key, revi_key), f, pickle.HIGHEST_PROTOCOL)

    convert_pd()

    remap_id()
