#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/8/6
import time
import os
from rich.progress import track
import torch
import numpy as np

print('began load models')
model = torch.load('./models/2023-08-06_015426.pth')
# model = torch.load('./models/2023-08-06_015426.pth')
# model = torch.load('./models/2023-08-06_023408.pth')
model.eval()
print('finish load models')


def model_test(audio):
    audio = np.array(audio).flatten()
    # print(audio.shape)
    audio = torch.tensor(audio)

    with torch.no_grad():
        output = model(audio)
        # print(output)

        _, predicted = torch.max(output, 1)  # 取得分最高的类别
        return predicted.item()

        # value = output.view(-1).tolist()
        # i = value.index(max(value))
        # print(i)

        # for i in range(37):
        #     i_label = torch.tensor([i])
        #     print(i_label)
        #     if torch.eq(i_label, output):
        #         print(i)
        #         print("正确")
        # print("你敲了: ", output)


from utils.dataset_ import read_data
# 取众数
from collections import Counter

DATASET_BASE = './dataset'
csv_files = [_ for _ in os.listdir(DATASET_BASE) if _.endswith('.csv')]
for c in csv_files:
    data = read_data(os.path.join(DATASET_BASE, c))
    res = [model_test(i) for i in data]
    res = Counter(res).most_common(1)[0][0]
    print(c, res)
