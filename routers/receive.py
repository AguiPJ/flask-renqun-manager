import time

from bson import ObjectId
from flask import Blueprint

from utils import req, getTime
from utils.mongodb import receiveTable, find

receive_opt = Blueprint('jieshou_opt ', __name__)


@receive_opt.get('/get/<int:page>/<int:pageSize>')
def get_table(page, pageSize):
    data = [i for i in receiveTable.find({}).sort("updateTime", -1).skip((page - 1) * pageSize).limit(pageSize)]
    for item in data:
        item['_id'] = str(item['_id'])
    return {"data": data, "total": receiveTable.count()}


@receive_opt.post('/append')
def append_table():
    data = req()
    t = getTime()
    data["updateTime"] = t
    data["createTime"] = t
    data["status"] = "接收中",
    receiveTable.insert_one(data)
    return {"data": "append success!", "code": 200}


@receive_opt.get('/delete/<bid>')
def delete_table(bid):
    r = find(receiveTable, {"_id": ObjectId(bid)})
    if len(r) > 0:
        receiveTable.delete_one({"_id": ObjectId(bid)})
        return {"data": "remove ok!", "code": 200}
    else:
        return {"data": "not find this obj", "code": 502}


@receive_opt.post('/update')
def update_table():
    data = req()
    data["_id"] = ObjectId(data['_id'])
    query = {"_id": data['_id']}
    data["updateTime"] = getTime()
    res = find(receiveTable, query)
    if len(res) > 0:
        receiveTable.update(query, data)
        return {"data": "update success!", "code": 200}
    else:
        return {"data": "not find this object!", "code": 502}
