
class LinksEntriesTable:
    def __init__(self, db):
        self.db = db
        self.collection = db.database['links_entries']

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
                self.db.changes.add(semester, prefix, key, old_value, new_value,
                                    user_args)
        # todo: send message to telegram
