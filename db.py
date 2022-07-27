from asyncio.windows_events import NULL
from pymongo import MongoClient

# connection using MongoClient
from pymongo import MongoClient


class Admin:
    def __init__(self):
        # mongodb url to connect python to mongodb using pymongo
        self.connection_string = "mongodb://localhost:27017/registration"
        self.collection_name = "users"
        self.database = "registeration"

    def get_database(self):
        client = MongoClient(self.connection_string)
        return client[self.database]

    def setCollection(self, db):
        # Get the database
        self.dbname = db
        self.collection = self.dbname[self.collection_name]

    def insertUser(self, user):
        return self.collection.insert_one(user)

    def deleteUser(self, email):
        return self.collection.delete_one({"email": email})

    def updateUser(self, email, status):
        return self.collection.update_one({"email": email}, {"$set": {"verified": status}})

    def getUsers(self):
        return self.collection.find({}, {"_id": 0, "roll": 1, "name": 1, "email": 1, "password": 1})

    def getUser(self, email):
        return self.collection.findOne({"email": email})
