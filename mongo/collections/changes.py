from datetime import datetime


class ChangesTable:
    def __init__(self, db):
        self.db = db
        self.collection = db.database['changes']

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

