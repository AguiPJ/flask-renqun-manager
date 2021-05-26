from bson import ObjectId
from flask import Blueprint

from utils import req
from utils.mongodb import RenQunManagerDB, find

jieshou_opt = Blueprint('jieshou_opt ', __name__)


@jieshou_opt.get('/get')
def get_table():
    data = find(RenQunManagerDB, sort=("updateTime", -1))
    return {"data": data}


@jieshou_opt.post('/append')
def append_table():
    data = req()
    RenQunManagerDB.insert_one(data)
    return {"data": "append success!", "code": 200}


@jieshou_opt.get('/delete/<bid>')
def delete_table(bid):
    r = find(RenQunManagerDB, {"_id": ObjectId(bid)})
    if len(r) > 0:
        RenQunManagerDB.delete_one({"_id": ObjectId(bid)})
        return {"data": "remove ok!", "code": 200}
    else:
        return {"data": "not find this obj", "code": 502}


@jieshou_opt.post('/update')
def update_table():
    data = req()
    print(data)
    return "data"
