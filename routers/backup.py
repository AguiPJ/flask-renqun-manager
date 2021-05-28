from flask import Blueprint

from utils.mongodb import receiveTable, historicalTable, locationTable, find

backup_opt = Blueprint('backup_opt ', __name__)


@backup_opt.get('/get')
def get_table():
    data = [i for i in find(historicalTable)] + [i for i in find(receiveTable)] + [i for i in find(locationTable)]
    return {"data": data}


@backup_opt.get('/autoBackup')
def autoBackup():
    return {"data": "auto Backup ok!", "code": 200}
