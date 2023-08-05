#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/8/5
import os
import pandas as pd
import numpy as np
import torch


def get_data_names():
    files = os.listdir('.')
    csv_files = [_ for _ in files if _.endswith('.csv')]
    return {
        int(file_name[:2]): file_name for file_name in csv_files
    }


def split(keys, values):
    from torch.utils.data import TensorDataset, DataLoader

    # 划分训练集和测试集
    train_ratio = 0.8  # 训练集占比
    train_size = int(train_ratio * n)
    test_size = n - train_size
    train_data, test_data = torch.utils.data.random_split(values, [train_size, test_size])
    train_target, test_target = torch.utils.data.random_split(keys, [train_size, test_size])

    print(train_data.shape, train_target.shape)

    # 定义训练集和测试集的数据加载器
    batch_size = 32
    train_loader = DataLoader(TensorDataset(train_data, train_target), batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(TensorDataset(test_data, test_target), batch_size=batch_size, shuffle=False)


def deal_1():
    # 处理最后的脏值
    import csv
    for target, file_name in get_data_names().items():
        if target == 11:
            print(target, file_name)
            data = []
            with open(file_name, 'r+') as f:
                # print(len(f.readlines()))
                data.extend(f.readlines())
                print(data)
                with open('out.csv', 'w') as f:
                    writer = csv.writer(f)
                    for i in data:
                        writer.writerow(i)

if __name__ == '__main__':
    # print(get_data_names())

    deal_1()
    from loguru import logger

    # print(pd.read_csv('01_1b22.csv'))
