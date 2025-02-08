from django.conf import settings
from pymongo import MongoClient

from mongo.collections.changes import ChangesTable
from mongo.collections.entries import EntriesTable
from mongo.collections.groups import GroupsTable
from mongo.collections.subjects import SubjectsTable
from mongo.collections.visits import VisitsTable


class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_CLUSTER_SECRET)
        self.database = self.client['nure_links']
        self.groups = GroupsTable(self)
        self.subjects = SubjectsTable(self)
        self.entries = EntriesTable(self)
        self.changes = ChangesTable(self)
        self.visits = VisitsTable(self)


db = MongoDB()
