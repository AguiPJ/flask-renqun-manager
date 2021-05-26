from pymongo import MongoClient

from config import MONGO_URL


def Mongo(table='db'): return MongoClient(f'mongodb://{MONGO_URL}', serverSelectionTimeoutMS=5000)["pack"][table]


RenQunManagerDB = Mongo('RenQunManager')


def find(DB: MongoClient, query=None, sort=None):
    if query is None:
        query = {}
    if sort:
        localData = [i for i in DB.find(query).sort(sort[0], sort[1])]
    else:
        localData = [i for i in DB.find(query)]
    for item in localData:
        item['_id'] = str(item['_id'])
    return localData
