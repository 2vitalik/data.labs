

class SubjectsTable:
    def __init__(self, db):
        self.db = db
        self.collection = db.database['subjects']

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

