from datetime import datetime

from django.conf import settings

from mongo.db import db


def create_subjects(prefix, subjects_names):
    subjects = []
    for short, long in subjects_names.items():
        subjects.append({
            'semester': settings.SEMESTER,
            'prefix': prefix,
            'short': short,
            'long': long,
            'created_at': datetime.now(),
        })

    db.subjects.add_many(subjects)
