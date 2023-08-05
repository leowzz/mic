#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/8/5

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from torchvision.transforms import transforms


class CustomDataset(Dataset):
    target = []
    data = []

    def add_dateset(self, target, data):
        self.target.extend(target)
        self.data.extend(data)

    # def to_tensor(self):
    #     self.new_data = []
    #     for i in self.data:
    #         item = np.array(i, dtype=np.float32)
    #         item = torch.tensor(item)
    #         self.new_data.append(item)
    #     self.data = self.new_data
    #     self.target
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = self.data[idx]
        y = self.target[idx]
        x = np.array(x).flatten()
        # x = np.transpose(x)
        x = torch.tensor(x)
        # y = torch.tensor(y)
        return x, y


class Tudui(nn.Module):
    def __init__(self, vocab_size, embedding_dim, num_filters, kernel_sizes, output_dim, dropout):
        super(Tudui, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.convs = nn.ModuleList(
            [nn.Conv1d(in_channels=embedding_dim, out_channels=num_filters, kernel_size=ks) for ks in kernel_sizes])
        self.conv2 = nn.Conv1d(in_channels=num_filters, out_channels=num_filters, kernel_size=3,
                               padding=1)  # Additional convolution layer
        self.conv3 = nn.Conv1d(in_channels=num_filters, out_channels=num_filters, kernel_size=5,
                               padding=2)  # Additional convolution layer
        self.fc = nn.Linear(len(kernel_sizes) * num_filters, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, text):
        embedded = self.embedding(text)
        embedded = embedded.permute(0, 2, 1)  # Permute to match Conv1d input shape (batch_size, embedding_dim, seq_len)
        conved = [nn.functional.relu(conv(embedded)) for conv in self.convs]
        pooled = [nn.functional.max_pool1d(conv, conv.shape[2]).squeeze(2) for conv in conved]
        cat = self.dropout(torch.cat(pooled, dim=1))
        return self.fc(cat)


class VoltageSensorModel(nn.Module):
    def __init__(self, input_size=3, hidden_size=16, output_size=1):
        super(VoltageSensorModel, self).__init__()
        self.hidden_size = hidden_size
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.rnn(x)
        out = self.fc(out[:, -1, :])
        return out


class MyModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MyModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.conv1 = nn.Conv2d(3, 3, 3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 3, 3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(2, 2)
        self.fc = nn.Linear(32 * 8 * 8, 36)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        x = x.view(-1, 32 * 8 * 8)
        x = self.fc(x)
        return x
