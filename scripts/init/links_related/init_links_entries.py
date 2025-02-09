import utils.django_bin

from mongo.db import db
from scripts.init.links_related.src.read_texts import read_subjects_texts, read_groups_splits
from scripts.init.links_related.src.parse_subjects import parse_subjects
from scripts.init.links_related.src.create_links_entries import create_links_entries


def init_links_entries():
    subjects_texts = read_subjects_texts()

    for prefix, subjects_text in subjects_texts.items():
        subjects_data, _ = parse_subjects(prefix, subjects_text)

        split, total = db.group_prefixes.get_split_total(prefix)

        if split:
            create_links_entries(prefix, subjects_data, 'eng',
                                 f'1-{split}', lambda x: 1 <= x <= split)
            create_links_entries(prefix, subjects_data, 'ukr',
                                 f'{split+1}-{total}', lambda x: split < x <= total)
        else:
            create_links_entries(prefix, subjects_data, 'core',
                                 f'1-{total}', lambda x: 1 <= x <= total)

        create_links_entries(prefix, subjects_data, 'alt',
                             f'0', lambda x: x == 0)


if __name__ == '__main__':
    init_links_entries()
