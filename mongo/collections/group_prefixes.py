import secrets
import string
from datetime import datetime

from django.conf import settings


class GroupPrefixesTable:
    def __init__(self, db):
        self.db = db
        self.collection = db.database['group_prefixes']

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
        group = self.collection.find_one({'key': key})
        if not group:
            return None, None
        return group.get('semester'), group.get('prefix')
