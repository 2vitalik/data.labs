import re
from collections import defaultdict
from pprint import pprint


def defaultdict_to_dict(dd):
    if isinstance(dd, defaultdict):
        dd = {k: defaultdict_to_dict(v) for k, v in dd.items()}
    return dd


def create_dict(entries):
    subjects = defaultdict(lambda: defaultdict(list))

    for entry in entries:
        subject = entry['subject']
        category = entry['category']
        title = entry['title']
        teacher = entry['teacher']
        links = entry['links']

        subjects[subject][category].append({
            'title': title,
            'teacher': teacher,
            'links': links,
        })

    subjects = defaultdict_to_dict(subjects)
    # pprint(subjects)
    return subjects


def title_sort_key(entry):
    title = entry['title']

    for index, prefix in enumerate(['Загальне', 'Лекції', 'ПЗ', 'ЛБ']):
        if title.startswith(prefix):
            priority = index
            break
    else:
        priority = float('inf')

    m = re.search(r'\((\d+)', title)
    group_number = int(m.group(1)) if m else 0

    return priority, group_number, title


def subject_sort_key(pair):
    subject = pair[0]
    if subject in ['ІМ', 'ІМ1п', 'ІМ2п', 'ФВ']:
        return 3, subject
    if subject.startswith('*'):
        return 2, subject
    return 1, subject


def prepare_entries(entries):
    """
    Prepare entries for displaying in the frontend (django templates).
    {
        'subject1': {
            'eng':  [{'title': ..., 'teacher': ..., 'links': ...}],
            'ukr':  [{'title': ..., 'teacher': ..., 'links': ...}],
            'alt':  [{'title': ..., 'teacher': ..., 'links': ...}],
            'core': [{'title': ..., 'teacher': ..., 'links': ...}],
        },
        'subject2': {
            ...
        },
        ...
    }

    :param entries:
        List of links entries from the database

    :return:
        Dictionary of subjects with lists of categories data
    """
    subjects = create_dict(entries)
    subjects = dict(sorted(subjects.items(), key=subject_sort_key))

    for subject, data in subjects.items():
        for category in data.keys():
            data[category] = list(sorted(data[category], key=title_sort_key))

    return subjects
