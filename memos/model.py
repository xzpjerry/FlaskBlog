import pymongo
from pymongo import MongoClient
from pymongo import IndexModel, ASCENDING, DESCENDING
import sys
import logging

class DB_config:

    def __init__(self, user, userpw, dbhost, dbport, dbname):
        self.url = "mongodb://%s:%s@%s:%s/%s" % (
            user, userpw, dbhost, dbport, dbname)
        self.user = user
        self.userpw = userpw
        self.dbhost = dbhost
        self.dbport = dbport
        self.dbname = dbname


class record:

    def __init__(self, date, title=None, text=None): # Inputed date will always be in unix timestamp format
        self.date = date
        if title:
            self.title = title
        if text:
            self.text = text

    def formatted(self):
        temp = {"type": "dated_memo",
                "date": self.date
                }
        if hasattr(self, 'title'):
            temp["title"] = self.title
        if hasattr(self, 'text'):
            temp["text"] = self.text
        return temp

    def __str__(self):
        return str(self.formatted())


class DB:

    def __init__(self, config : DB_config):
        try:
            self.db = getattr(MongoClient(config.url), config.dbname)
            self.collection = None
            logging.info("Collection is not yet set for now.")
        except:
            logging.warning(
                "Can not connect to the Database, please check your config.")
            sys.exit(1)

    def set_collection(self, collection):
        try:
            self.collection = getattr(self.db, collection)
            index = IndexModel([("date", DESCENDING)])
            self.collection.create_indexes([index])
        except:
            logging.warning(
                "Can not connect to the collection or the collection is not existed? Do you have permission to write?.")
            raise
        finally:
            logging.info("Now the collection is set.")
            for index in self.collection.list_indexes():
                logging.info("Using index: " + str(index))

    def del_collection(self):
        if self.collection != None:
            try:
                self.collection.drop()
            except Exception as e:
                logging.warning("Deletion failed.")
                raise
            finally:
                logging.info("DB deleted.")

    def delete_memos(self, record):
        if self.collection != None:
            try:
                self.collection.delete_many(record.formatted())
            except:
                logging.warning(
                    "Can not connect to the collection, is the collection exist? Do you have permission to write?.")
                raise
            finally:
                logging.info("All related records deleted.")
        else:
            logging.warning("Collection is not yet set.")
            logging.warning("Nothing to delete.")

    def insert(self, new_record):
        if self.collection != None:
            try:
                logging.info("Inserting " + str(new_record))
                self.collection.insert(new_record.formatted())
            except:
                logging.warning(
                    "Can not connect to the collection, is the collection exist? Do you have permission to write?.")
                logging.warning("Insertion failed.")
                raise
            finally:
                logging.info("Record inserted.")
        else:
            logging.warning("Collection is not yet set.")
            logging.warning("Insertion failed.")

    def get(self, record, title):
        try:
            print(record)
            result = self.collection.find_one(record)
            del result['_id']
            return result
        except:
            logging.warning(
                "Can not connect to the collection, is the collection exist? Do you have permission to write?.")
            logging.warning("Fetch failed.")
            raise
        finally:
            logging.info("Found and returned!")

    def get_all(self):
        if self.collection != None:
            try:
                records = []
                for onerecord in self.collection.find().sort([("date", DESCENDING)]):
                    del onerecord['_id']
                    records.append(onerecord)
            except:
                logging.warning(
                    "Can not connect to the collection, is the collection exist? Do you have permission to write?.")
                logging.warning("Fetch failed.")
                raise
            finally:
                return records
        else:
            logging.warning("Collection is not yet set.")
            logging.warning("Finding failed.")
