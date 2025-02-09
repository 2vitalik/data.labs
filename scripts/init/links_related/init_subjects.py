import utils.django_bin

from mongo.db import db
from scripts.init.links_related.links_entries_steps.s1_read_data import read_subjects_texts
from scripts.init.links_related.subjects.parse import parse_subjects


def init_subjects():
    subjects_texts = read_subjects_texts()

    for prefix, subjects_text in subjects_texts.items():
        _, subjects_names = parse_subjects(prefix, subjects_text)

        for short, long in subjects_names.items():
            db.subjects.add(prefix, short, long)


if __name__ == '__main__':
    init_subjects()
