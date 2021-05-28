from bson import ObjectId
from flask import Blueprint

from utils import req, getTime
from utils.mongodb import locationTable, find

location_opt = Blueprint('location_opt ', __name__)


@location_opt.post('/append')
def append_table():
    data = req()
    t = getTime()
    data["updateTime"] = t
    data["createTime"] = t
    locationTable.insert_one(data)
    return {"data": "append success!", "code": 200}


@location_opt.get('/get/<int:page>/<int:pageSize>')
def get_table(page, pageSize):
    data = [i for i in locationTable.find({}).sort("updateTime", -1).skip((page - 1) * pageSize).limit(pageSize)]
    for item in data:
        item['_id'] = str(item['_id'])
    return {"data": data, "total": locationTable.count()}


@location_opt.get('/delete/<bid>')
def delete_table(bid):
    r = find(locationTable, {"_id": ObjectId(bid)})
    if len(r) > 0:
        locationTable.delete_one({"_id": ObjectId(bid)})
        return {"data": "remove ok!", "code": 200}
    else:
        return {"data": "not find this obj", "code": 502}


@location_opt.post('/update')
def update_table():
    data = req()
    data["_id"] = ObjectId(data['_id'])
    query = {"_id": data['_id']}
    data["updateTime"] = getTime()
    res = find(locationTable, query)
    if len(res) > 0:
        locationTable.update(query, data)
        return {"data": "update success!", "code": 200}
    else:
        return {"data": "not find this object!", "code": 502}
