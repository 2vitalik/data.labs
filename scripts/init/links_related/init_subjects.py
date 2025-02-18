import utils.django_bin

from mongo.db import db
from scripts.init.links_related.src.read_texts import read_subjects_texts
from scripts.init.links_related.src.parse_subjects import parse_subjects


def init_subjects():
    subjects_texts = read_subjects_texts()

    for prefix, subjects_text in subjects_texts.items():
        print('Prefix:', prefix)
        _, subjects_names = parse_subjects(prefix, subjects_text)

        for short, long in subjects_names.items():
            print('- Subject:', short, '-', long)
            if not db.subjects.exists(prefix, short):
                db.subjects.add(prefix, short, long)
                print('  [+] Added')
            else:
                print('  [-] Already exists')


if __name__ == '__main__':
    init_subjects()
