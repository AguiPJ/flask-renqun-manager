import random
import time
from json import loads

from flask import request

randomDataStart = 100
randomDataEnd = 300


def randomData():
    dataList = []
    for i in range(10):
        i = random.randrange(randomDataStart, randomDataEnd)
        dataList.append(i)
    return dataList


def req():
    return loads(request.get_data())


def getTime(): return int(round(time.time() * 1000))
