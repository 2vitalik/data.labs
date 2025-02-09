import utils.django_bin
from datetime import datetime

from django.conf import settings

from mongo.db import db
from scripts.init.links_related.links_entries_steps.s1_read_data import read_data
from scripts.init.links_related.subjects.parse import parse_subjects


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


def init_subjects():
    groups_splits, subjects_texts = read_data()

    for prefix, subjects_text in subjects_texts.items():
        _, subjects_names = parse_subjects(prefix, subjects_text)
        create_subjects(prefix, subjects_names)


if __name__ == '__main__':
    init_subjects()
