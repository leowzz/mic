import serial as ser
import time

se = ser.Serial('/dev/ttyTHS0', 115200, timeout=1)

# Wait a second to let the port initialize
time.sleep(.5)

def get_ser_info():
    res = []
    print("wait data")
    # while 1:
    for i in range(20000):
        if se.inWaiting() > 0:
            data = se.readline()
            data_str = str(data)
            if '\\xb' in data_str:
                data_str = data_str[2:-3].replace('\\xb', '')
            data_list = data.decode('ascii')[:-1].split(',')
            res.append(data_list)
    # 清空串口缓存
    se.flushInput()
    return res[1:]

import uuid
import datetime


def get_uuid(bit: int=4):
    return str(uuid.uuid4())[:bit]

def get_now():
    return f"{datetime.datetime.now():%Y-%m-%d_%H%M%S}"

"""
hex(ord("("))
"""

if __name__ == "__main__":
    f = open(f'./data/rec{get_now()}_{get_uuid()}.txt', 'a')
    try:
        se.flushInput()
        while 1:
            datas = get_ser_info()
            f.write(str(datas))
            print(datas)
            input('请按任意键')
    
    finally:
        f.close()
        se.close()
    