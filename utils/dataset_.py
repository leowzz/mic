#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/8/5
import os
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader, TensorDataset


def get_data_names():
    files = os.listdir('./data')
    print(files)
    return {
        int(_[:2]): f"data/{_}" for _ in files if _.endswith('.csv')
    }


def split_dataset(dataset, batch_size):
    # 划分训练集和测试集
    train_ratio = 0.8  # 训练集占比
    n = len(dataset)
    train_size = int(train_ratio * n)
    test_size = n - train_size
    train_data, test_data = torch.utils.data.random_split(dataset, [train_size, test_size])

    # 定义训练集和测试集的数据加载器
    # batch_size = 32
    train_loader = DataLoader(dataset=train_data, batch_size=batch_size)
    test_loader = DataLoader(test_data, batch_size=batch_size)
    return train_loader, test_loader


import csv
import os


def deal_1(base_dir, filenames, output_dir):
    # 处理最后一行的脏值
    for file_name in filenames:
        print(file_name)
        target = int(file_name[:2])
        print(target, file_name)
        data = []
        # 读取文件
        with open(os.path.join(base_dir, file_name), 'r+', encoding='utf-8') as f:
            data.extend(f.readlines())
            # 输出文件
            with open(os.path.join(output_dir, f'{target:03d}.csv'), 'w') as f1:
                for i in data[:-1]:
                    f1.write(i)


def read_data(filepath):
    data = pd.read_csv(filepath)

    # 结果值
    res = []
    # 每段音频
    item = []
    # 计数器, 用来判断是否结束取值
    count_ = 0
    i = 0
    # 假如数据在范围内开始取值 存到item 里面, 直到连续的5个数据不在范围内, 就将item存到res里面
    # 重复上面的步骤, 直到数据取完
    while i < len(data.values):
        line = data.values[i]
        if min(line) < 800 or max(line) > 2000:
            while i < len(data.values):
                line = data.values[i]
                if min(line) < 800 or max(line) > 2000:
                    item.append(line.tolist())
                    i += 1
                else:
                    count_ += 1
                if count_ > 5:
                    res.append(item)
                    item = []
                    count_ = 0
                    break
        i += 1
    print(filepath, len(res))
    print([len(i) for i in res])
    # res = [_[:60] for _ in res if 60 < len(_) < 120]

    return res


if __name__ == '__main__':
    ...
    # print(get_data_names())
    # 处理错误值
    # deal_1()

    # main('001.csv')
    # print(pd.read_csv('01_1b22.csv'))

    DATASET_BASE = '../dataset'
    csv_files = [_ for _ in os.listdir(DATASET_BASE) if _.endswith('.csv')]
    for c in csv_files:
        read_data(os.path.join(DATASET_BASE, c))
