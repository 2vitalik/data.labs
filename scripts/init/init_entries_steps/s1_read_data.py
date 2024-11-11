import re
from os.path import join

from django.conf import settings


def read_file(filename):
    filepath = join('data', settings.SEMESTER, filename)
    return open(filepath, encoding='utf-8').read().strip()


def read_groups_splits():
    group_splits = {}

    for line in read_file('groups-splits.txt').split('\n'):
        group, data = line.split(': ')
        split, total = data.split(' ')
        group_splits[group] = int(split), int(total)

    return group_splits


def read_subjects_texts():
    subjects = {}

    for data in read_file('subjects-texts.txt').split('\n\n'):
        prefix, group_data = data.split('\n', 1)

        m = re.fullmatch(r'\[(.*)]', prefix)
        if not m:
            raise Exception(f'Wrong `prefix` format: "{prefix}"')
        prefix = m.group(1)

        subjects[prefix] = group_data

    return subjects


def read_data():
    return read_groups_splits(), read_subjects_texts()
