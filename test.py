#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/8/6

import serial as ser
import time

se = ser.Serial('/dev/ttyTHS0', 115200, timeout=1)

# Wait a second to let the port initialize
time.sleep(.5)


def get_ser_info():
    res = []
    print("wait data")
    temp = []
    # while 1:
    for i in range(1000):
        if se.inWaiting() > 0:
            data = se.readline()
            temp.append(data)
    print('read over')
    for data in temp[1:]:
        try:
            item = list(map(int, data.decode('ascii')[:-1].split(',')))
        except UnicodeDecodeError:
            continue
        res.append(item)
    # 清空串口缓存
    se.flushInput()
    return res


import uuid
import datetime


def get_uuid(bit: int = 4):
    return str(uuid.uuid4())[:bit]


def get_now():
    return f"{datetime.datetime.now():%Y-%m-%d_%H%M%S}"


"""
hex(ord("("))
"""

if __name__ == "__main__":
    f = open(f'./data/rec{get_now()}_{get_uuid()}.txt', 'a')
    se.flushInput()
    time.sleep(.2)

    try:
        while 1:
            datas = get_ser_info()
            if len(datas) == 0:
                continue
            max_ = [
                max(datas, key=lambda x: x[i]) for i in range(3)
            ]
            for i in max_:
                print(i)
            print()

            min_ = [
                min(datas, key=lambda x: x[i]) for i in range(3)
            ]

            for i in min_:
                print(i)
            print('\n')
            # print([i[0] for i in sort_])
            indexs = [datas.index(i) for i in max_]
            print(indexs)
            indexs = [datas.index(i) for i in min_]
            print(indexs)

            f.write(str(datas))
            se.flushInput()
            # print(datas)
            input('请按任意键')

    finally:
        f.close()
        se.flushInput()
        se.close()

# while i < len(data.values):
#     line = data.values[i]
#     if min(line) < 800 or max(line) > 2000:
#         while i < len(data.values):
#             line = data.values[i]
#             if min(line) < 800 or max(line) > 2000:
#                 item.append(line.tolist())
#                 i += 1
#             else:
#                 count_ += 1
#             if count_ > 15:
#                 res.append(item)
#                 item = []
#                 count_ = 0
#                 break
#     i += 1