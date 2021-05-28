from bson import ObjectId
from flask import Blueprint

from utils import req, getTime
from utils.mongodb import historicalTable, find

historical_opt = Blueprint('historical_opt ', __name__)


@historical_opt.post('/append')
def append_table():
    data = req()
    t = getTime()
    data["updateTime"] = t
    data["createTime"] = t
    historicalTable.insert_one(data)
    return {"data": "append success!", "code": 200}


@historical_opt.get('/get/<int:page>/<int:pageSize>')
def get_table(page, pageSize):
    data = [i for i in historicalTable.find({}).sort("updateTime", -1).skip((page - 1) * pageSize).limit(pageSize)]
    for item in data:
        item['_id'] = str(item['_id'])
    return {"data": data, "total": historicalTable.count()}


@historical_opt.get('/delete/<bid>')
def delete_table(bid):
    r = find(historicalTable, {"_id": ObjectId(bid)})
    if len(r) > 0:
        historicalTable.delete_one({"_id": ObjectId(bid)})
        return {"data": "remove ok!", "code": 200}
    else:
        return {"data": "not find this obj", "code": 502}


@historical_opt.post('/update')
def update_table():
    data = req()
    data["_id"] = ObjectId(data['_id'])
    query = {"_id": data['_id']}
    data["updateTime"] = getTime()
    res = find(historicalTable, query)
    if len(res) > 0:
        historicalTable.update(query, data)
        return {"data": "update success!", "code": 200}
    else:
        return {"data": "not find this object!", "code": 502}
