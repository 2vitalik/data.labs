import utils.django_bin

from scripts.init.links_entries_steps.s1_read_data import read_data
from scripts.init.subjects.parse import parse_subjects
from scripts.init.init_subjects import create_subjects
from scripts.init.links_entries_steps.s4_create_links_entries import create_links_entries


def init_links_entries():
    groups_splits, subjects_texts = read_data()

    for prefix, subjects_text in subjects_texts.items():
        subjects, subjects_names = parse_subjects(prefix, subjects_text)
        create_subjects(prefix, subjects_names)

        split, total = groups_splits[prefix]

        if split:
            create_links_entries(prefix, subjects, 'eng',
                                 f'1-{split}', lambda x: 1 <= x <= split)
            create_links_entries(prefix, subjects, 'ukr',
                                 f'{split+1}-{total}', lambda x: split < x <= total)
        else:
            create_links_entries(prefix, subjects, 'core',
                                 f'1-{total}', lambda x: 1 <= x <= total)

        create_links_entries(prefix, subjects, 'alt',
                             f'0', lambda x: x == 0)


if __name__ == '__main__':
    init_links_entries()
