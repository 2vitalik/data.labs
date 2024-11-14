import secrets
import string
from datetime import datetime

from django.conf import settings
from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_CLUSTER_SECRET)
        self.db = self.client['nure_links']
        self.groups = GroupsTable(self.db['groups'])
        self.subjects = SubjectsTable(self.db['subjects'])
        self.entries = EntriesTable(self.db['entries'])
        self.changes = ChangesTable(self.db['changes'])


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
        group = self.collection.find_one({'key': key})
        if not group:
            return None, None
        return group.get('semester'), group.get('prefix')


class SubjectsTable:
    def __init__(self, collection):
        self.collection = collection

    def add_many(self, subjects):
        self.collection.insert_many(subjects)

    def get(self, semester, prefix):
        subjects = self.collection.find({
            'semester': semester,
            'prefix': prefix,
        })
        return {
            subject.get('short'): subject.get('long')
            for subject in subjects
        }


class EntriesTable:
    def __init__(self, collection):
        self.collection = collection

    def add_many(self, entries):
        self.collection.insert_many(entries)

    def get(self, semester, prefix):
        return self.collection.find({
            'semester': semester,
            'prefix': prefix,
        })

    def get_data(self, semester, prefix):
        entries = self.get(semester, prefix)
        data = {}
        for entry in entries:
            subject = entry.get('subject')
            category = entry.get('category')
            title = entry.get('title')
            teacher = entry.get('teacher')
            links = entry.get('links')
            data[f'{subject}|{category}|{title}|{teacher}'] = links
        return data

    def edit(self, semester, prefix, new_data, user_args):
        old_data = self.get_data(semester, prefix)
        for key, new_value in new_data.items():
            if key == 'csrfmiddlewaretoken':
                continue

            subject, category, title, teacher = key.split('|')
            old_value = old_data.get(key)

            if old_value != new_value:
                self.collection.update_one({
                    'semester': semester,
                    'prefix': prefix,
                    'subject': subject,
                    'category': category,
                    'title': title,
                    'teacher': teacher,
                }, {
                    '$set': {
                        'links': new_value,
                    }
                })
                db.changes.add(semester, prefix, key, old_value, new_value,
                               user_args)
        # todo: send message to telegram


class ChangesTable:
    def __init__(self, collection):
        self.collection = collection

    def add(self, semester, prefix, key, old_value, new_value, user_args):
        subject, category, title, teacher = key.split('|')
        self.collection.insert_one({
            'semester': semester,
            'prefix': prefix,
            'subject': subject,
            'category': category,
            'title': title,
            'teacher': teacher,
            'old_links': old_value,
            'new_links': new_value,
            **user_args,
            'created_at': datetime.now(),
        })


db = MongoDB()
