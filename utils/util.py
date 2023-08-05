#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/8/5
import time
import uuid
import datetime


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f"{func.__name__} cost {time.time() - start} s")
        return res

    return wrapper


def get_uuid(bit: int = 4):
    return str(uuid.uuid4())[:bit]


def get_now():
    return f"{datetime.datetime.now():%Y-%m-%d_%H%M%S}"


def translate(data):
    x = data % 6
    if x == 0:
        x = 6
    y = data // 6 + 1

    x_dict = [0, 'AB', 'CD', 'EF', 'GH', 'IJ', 'KL']
    y_dict = [0, '0102', '0304', '0506', '0708', '0910', '1112']
    print(f'{x_dict[x]}{y_dict[y]}')
    # if data % 6 == 1:
    #     print('1')


if __name__ == '__main__':
    # for i in range(1, 37):
    translate(10)
