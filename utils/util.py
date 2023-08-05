#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/8/5
import time


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f"{func.__name__} cost {time.time() - start} s")
        return res

    return wrapper
def get_uuid(bit: int=4):
    return str(uuid.uuid4())[:bit]

def get_now():
    return f"{datetime.datetime.now():%Y-%m-%d_%H%M%S}"