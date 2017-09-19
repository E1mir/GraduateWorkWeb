# -*- coding: utf-8 -*-
from flask_login import UserMixin
import pymongo
import datetime
from bson import ObjectId
from settings import DB_CONNECTION_STRING


class DatabaseConnector(object):
    def __init__(self, database_name, limit=1000):
        self.client = pymongo.MongoClient(DB_CONNECTION_STRING)
        self.database = self.client[database_name]
        self.limit = limit

    def insert(self, collection, insert_object):
        return self.database[collection].insert_one(insert_object).inserted_id

    def update(self, collection, upd_object):
        upd_object_id = ObjectId(upd_object["_id"])
        return self.database[collection].update_one(
            {"_id": upd_object_id},
            {"$set": upd_object},
            upsert=True
        )

    def save(self, collection, query_object, obj):
        return self.database[collection].update_one(
            query_object,
            {"$set": obj},
            upsert=True
        )

    def delete_by_object_id(self, collection, obj_id):
        return self.database[collection].delete_one({"_id": ObjectId(obj_id)})

    def list_by_query(self, collection, query_object):
        return self.database[collection].find(query_object)

    def count_by_query(self, collection, query_object):
        return self.database[collection].count(query_object)

    def collection(self, collection):
        return self.database[collection]


class CollectionModel(object):
    """
        Parent class for creating class and object instances of storage collection dict.
        Automatically create instance of class by it is fields.
    """

    def __init__(self, d):
        for item in self.__dict__:
            self.__dict__[item] = d.get(item, None)


class User(UserMixin):
    def __init__(self, _id, permission="default"):
        self.id = _id
        self.permission = permission


'''Database objects'''


class StorageAccountModel(CollectionModel):
    def __init__(self, d):
        self._id = None
        self.username = None
        self.email = None
        self.balance = None
        self.shop_name = None
        self.type = None
        self.permission = None
        super(StorageAccountModel, self).__init__(d)


class StorageTypeModel(CollectionModel):
    def __init__(self, d):
        self.name = None
        super(StorageTypeModel, self).__init__(d)


class StorageGoodsModel(CollectionModel):
    def __init__(self, d):
        self.name = None
        self.type = None
        self.price = None
        self.description = None
        self.count = None
        super(StorageGoodsModel, self).__init__(d)


class StorageOrderModel(CollectionModel):
    def __init__(self, d):
        self.order_id = None
        self.account = None
        self.total_cost = None
        self.date = None
        self.status = None
        self.order = None
        self.confirm_timestamp = None
        super(StorageOrderModel, self).__init__(d)
        self.confirm_date = self.get_confirm_date(self.confirm_timestamp)

    @staticmethod
    def get_confirm_date(timestamp):
        if timestamp != 0:
            return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d-%m-%Y %H:%M:%S')
        return ""


class WMSAccountsModel(object):
    def __init__(self):
        self.types = None
        self.permissions = None
        self.accounts = None


class WMSTypesModel(object):
    def __init__(self):
        self.types = None


class WMSWarehouseModel(object):
    def __init__(self):
        self.warehouse = None
        self.types = None


class WMSOrdersModel(object):
    def __init__(self):
        self.orders = None


''' Very simple encryption functions'''


def encrypt_pass(normal_password):
    encrypted_password = ""
    for d_char in normal_password:
        d_ch_id = ord(d_char)
        enc_id = d_ch_id + 5
        e_char = chr(enc_id)
        encrypted_password += e_char
    return encrypted_password
