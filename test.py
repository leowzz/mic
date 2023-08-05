import serial as ser
import time
from rich.progress import track
import torch
import numpy as np

se = ser.Serial(
    '/dev/ttyTHS0', 115200,
    bytesize=ser.EIGHTBITS,
    parity=ser.PARITY_NONE,
    stopbits=ser.STOPBITS_ONE,
)

print('begian load models')
# model = torch.load('./models/2023-08-06_015426.pth')
model = torch.load('./models/2023-08-06_015426.pth')
model.eval()
print('finish load models')


def model_test(audio):
    audio = np.array(audio).flatten()
    audio = np.transpose(audio)
    audio = torch.tensor(audio)
    with torch.no_grad():
        output = model(audio)
        print("你敲了: ", output)


def get_audio(data, f):
    # 每段音频
    audio = []
    # 计数器, 用来判断是否结束取值
    count_ = 0
    i = 0
    # 假如数据在范围内开始取值 存到audio 里面, 直到连续的5个数据不在范围内, 就将audio存到res里面
    # 重复上面的步骤, 直到数据取完
    while i < len(data):
        line = data[i]
        if min(line) < 800 or max(line) > 2000:
            while i < len(data):
                line = data[i]
                if min(line) < 800 or max(line) > 2000:
                    # 来, 存之
                    audio.append(line)
                    i += 1
                else:
                    count_ += 1
                if count_ > 15:
                    # 太多正常值了, 说明这段音频结束了
                    if 60 < len(audio) < 120:
                        res_ = model_test(audio[:60])
                        print(res_)
                        f.write(str(res_))
                    return True
        i += 1
    return False


# Wait a second to let the port initialize
# time.sleep(.5)
def get_ser_info(n, w=None):
    res = []
    item = None
    print("wait data")
    count_ = 0
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
                    count_ += 1
                    # print('item list', item_list)
                    # 将每一项转为list[int]
                    item = list(map(int, item_list))
                    res.append(item)
                    if count_ % 1000 == 0:
                        get_audio(res, w)
                        res = []
                # except UnicodeDecodeError or ValueError as e:
                except UnicodeDecodeError as e:
                    print(e)
                    continue
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
import csv


def main(f):
    time.sleep(.1)
    se.flushInput()
    time.sleep(.1)
    print(get_ser_info(100)[50:80])
    print(get_ser_info(100)[50:80])
    print(get_ser_info(100)[50:80])
    # 10000 5秒
    datas = get_ser_info(100000, f)
    if len(datas) == 0:
        print('break')
    se.flushInput()
    print('完事了, 歇一会')


if __name__ == "__main__":

    # file_name = int(input('输入文件名也就是这次的数据集标签 (例如1): '))
    f = open(f'./log/{get_now()}_{get_uuid()}.log', 'w')
    try:
        main(f)
    except UnicodeDecodeError as e:
        print(e)
    finally:
        f.close()
        se.flushInput()
        se.close()
