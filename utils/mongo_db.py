import secrets
import string
from datetime import datetime

from django.conf import settings
from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_CLUSTER)
        self.db = self.client['nure_links']
        self.groups = GroupsTable(self.db['groups'])


class GroupsTable:
    def __init__(self, collection):
        self.collection = collection

    def key(self):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(16))

    def add(self, prefix):
        self.collection.insert_one({
            'key': self.key(),
            'semester': settings.SEMESTER,
            'prefix': prefix,
            'created_at': datetime.now(),
        })

    def get(self, key):
        return self.collection.find_one({'key': key}).get('group')


db = MongoDB()
