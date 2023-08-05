#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/8/5
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from meta import CustomDataset, Model, MyModel, VoltageSensorModel, Tudui
from utils.dataset_ import get_data_names, split_dataset, deal_1, read_data
from utils.util import get_now, get_uuid

def train(model, optimizer, criterion, train_loader):
    model.train()

    for batch_idx, (data, targets) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, targets)
        loss.backward()
        optimizer.step()

        if batch_idx % 56 == 0:
            print(f'Loss: {loss.item()}')


def begin(train_loader, learning_rate=0.001, momentum=0.9, epoch=10):
    filename = f"{get_now()}{get_uuid()}"
    # 创建模型实例
    input_size = 3  # 输入大小，即传感器数量
    hidden_size = 16  # 隐藏层大小，可根据需求调整
    output_size = 1  # 输出大小，即传感器状态
    # model = VoltageSensorModel(input_size, hidden_size, output_size)
    model = Tudui(4000, 100, 32, [3, 4, 5], 36, 0.5)
    # 定义损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=momentum)

    # 开始训练
    for epoch in range(epoch):
        print(f'Epoch: {epoch + 1}')
        train(model, optimizer, criterion, train_loader)
        print('---------------------------')
        torch.save(model, f"models/{filename}.pth")


from utils.util import timeit


@timeit
def load_dataset():
    # my = []
    _dataset = CustomDataset()
    DATASET_BASE = './dataset'
    csv_files = [_ for _ in os.listdir(DATASET_BASE) if _.endswith('.csv')]
    for csv_file in csv_files[:2]:
        target = int(csv_file[:3])
        print(csv_file, target)
        audios = read_data(os.path.join(DATASET_BASE, csv_file))
        _dataset.add_dateset([target] * len(audios), audios)
        # my.append([target, len(audios)] )
    # print(my)
    # exit(1)
    return _dataset


if __name__ == '__main__':
    ...
    batch_size = 4
    learning_rate = 0.0001
    momentum = 0.6
    epoch = 180
    dataset = load_dataset()
    train_, test_ = split_dataset(dataset, batch_size)
    begin(train_, learning_rate, momentum, epoch)

    # deal_1('./data', os.listdir('data'), './dataset')

    # data = read_data('./dataset/001.csv')
    # dataset = CustomDataset(1, data)
    # test_split(dataset)

    # print(read_data('./dataset/001.csv'))
    # split(*get_data_names())
