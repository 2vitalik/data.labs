from datetime import datetime


class VisitsTable:
    def __init__(self, collection):
        self.collection = collection

    def add(self, path, user_args):
        self.collection.insert_one({
            'path': path,
            **user_args,
            'created_at': datetime.now(),
        })
