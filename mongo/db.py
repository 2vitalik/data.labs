from django.conf import settings
from pymongo import MongoClient

from mongo.collections.links_changes import LinksChangesTable
from mongo.collections.links_entries import LinksEntriesTable
from mongo.collections.group_prefixes import GroupPrefixesTable
from mongo.collections.subjects import SubjectsTable
from mongo.collections.visits import VisitsTable


class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_CLUSTER_SECRET)
        self.database = self.client['nure_links']
        self.group_prefixes = GroupPrefixesTable(self)
        self.subjects = SubjectsTable(self)
        self.links_entries = LinksEntriesTable(self)
        self.links_changes = LinksChangesTable(self)
        self.visits = VisitsTable(self)


db = MongoDB()
