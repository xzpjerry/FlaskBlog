import pymongo
from pymongo import MongoClient
import arrow
import sys
import uuid

import config
CONFIG = config.configuration()
import model

myconfig = model.DB_config(CONFIG.DB_USER,
    CONFIG.DB_USER_PW,
    CONFIG.DB_HOST, 
    CONFIG.DB_PORT, 
    CONFIG.DB)

test_case_amount = 100
time_stamps = []
test_DB = model.DB(myconfig)
test_DB.set_collection(uuid.uuid4().hex)

def test_insert():
    counter = 0
    assert len(test_DB.get_all()) == counter
    for i in range(test_case_amount):
        date = arrow.now().timestamp
        time_stamps.append(date)
        text = i
        test_DB.insert(model.record(date, text))
        counter += 1
        assert len(test_DB.get_all()) == counter

def test_read_del():
    assert len(test_DB.get_all()) == test_case_amount
    counter = 0
    for timestamp in time_stamps:
        test_DB.delete_memos(model.record(timestamp, counter))
        assert len(test_DB.get_all()) == test_case_amount - counter - 1
        counter += 1


test_DB.del_collection()
