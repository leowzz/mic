import serial as ser
import time
from rich.progress import track



se = ser.Serial(
        '/dev/ttyTHS0', 115200,
        bytesize=ser.EIGHTBITS,
        parity=ser.PARITY_NONE,
        stopbits=ser.STOPBITS_ONE,
    )
def get_bang():
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
                if count_ > 15:
                    res.append(item)
                    item = []
                    count_ = 0
                    break
        i += 1

# Wait a second to let the port initialize
#time.sleep(.5)
def get_ser_info(n, w=None):
    res = []
    print("wait data")
    temp = []
    # while 1:
    # for step in track(range(100)):
    #     do_step(step)
    item = []
    for i in track(range(n)):

        if i % 500 == 0:
            print(i)
            if item:
                print(item)
        if se.inWaiting() > 0:
            data = se.readline()
            if i > 2:
                try:
                    item_list = data.decode('ascii')[:-1].split(',')
                    # print('item list', item_list)
                    # 将每一项转为list[int]
                    item = list(map(int, item_list))
                    if min(item) < 800 or max(item) > 2000:
                        while i < len(data.values):
                            item = data.values[i]
                            if min(item) < 800 or max(item) > 2000:
                                item.append(item.tolist())
                                i += 1
                            else:
                                count_ += 1
                            if count_ > 15:
                                res.append(item)
                                item = []
                                count_ = 0
                                break
                    i += 1

                    if w:
                        w.writerow(item)
                    res.append(item)
                # except UnicodeDecodeError or ValueError as e:
                except Exception as e:
                    print(e)
                    continue
    return res

import uuid
import datetime


def get_uuid(bit: int=4):
    return str(uuid.uuid4())[:bit]

def get_now():
    return f"{datetime.datetime.now():%Y-%m-%d_%H%M%S}"

"""
hex(ord("("))
"""
import csv
def main(f):

    csv_writer = csv.writer(f)
    time.sleep(.1)
    se.flushInput()
    time.sleep(.1)
    print(get_ser_info(100)[50:80])
    print(get_ser_info(100)[50:80])
    print(get_ser_info(100)[50:80])
    # 10000 5秒
    datas = get_ser_info(100000, csv_writer)
    if len(datas) == 0:
        print('break')
    se.flushInput()
    print('完事了, 歇一会')

if __name__ == "__main__":

    file_name = int(input('输入文件名也就是这次的数据集标签 (例如1): '))
    f = open(f'./data/{file_name:02d}_{get_uuid()}.csv', 'w')
    try:
        main(f)
    except Exception as e:
        print(e)
    finally:
        f.close()
        se.flushInput()
        se.close()