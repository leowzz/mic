import serial as ser
import time
from rich.progress import track



se = ser.Serial(
        '/dev/ttyTHS0', 115200, timeout=1,
        bytesize=ser.EIGHTBITS,
        parity=ser.PARITY_NONE,
        stopbits=ser.STOPBITS_ONE,
    )

# Wait a second to let the port initialize
time.sleep(.5)

def get_ser_info(n, w=None):
    res = []
    print("wait data")
    temp = []
    # while 1:
    # for step in track(range(100)):
    #     do_step(step)
    for i in track(range(n)):
        if i % 500 == 0:
            print(i)
        if se.inWaiting() > 0:
            data = se.readline()
            temp.append(data)
            if i > 2:
                try:
                    item_list = data.decode('ascii')[:-1].split(',')
                    # print('item list', item_list)
                    item = list(map(int, item_list))
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
    se.flushInput()
    time.sleep(1)
    print(get_ser_info(100)[50:80])
    print(get_ser_info(100)[50:80])
    print(get_ser_info(100)[50:80])
    # 10000 5秒
    datas = get_ser_info(200000, csv_writer)
    if len(datas) == 0:
        print('break')
    f.write(str(datas))
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
    