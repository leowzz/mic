#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/8/5
import os
import pandas as pd
import numpy as np
import torch


def get_data_names():
    files = os.listdir('./data')
    print(files)
    return {
        int(_[:2]): f"data/{_}" for _ in files if _.endswith('.csv')
    }

def test_split(dataset):
    # 划分训练集和测试集
    train_ratio = 0.8  # 训练集占比
    n = len(dataset)
    train_size = int(train_ratio * n)
    test_size = n - train_size
    train_data, test_data = torch.utils.data.random_split(dataset, [train_size, test_size])
    print(f"{train_data=}")
    print(f"{test_data=}")

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

    res = [_ for _ in res if 50 < len(_) < 120]

    return res


if __name__ == '__main__':
    ...
    # print(get_data_names())
    # 处理错误值
    # deal_1()

    # main('001.csv')
    # print(pd.read_csv('01_1b22.csv'))
