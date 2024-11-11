import re
from collections import defaultdict
from pprint import pprint


def prettify_teacher(teacher_value):
    return ''.join([
        f'<span>{teacher}</span>'
        for teacher in teacher_value.split(', ')
    ])


def prettify_links(links):
    return links + 'todo'  # todo


def convert_to_dict(dd):
    if isinstance(dd, defaultdict):
        dd = {k: convert_to_dict(v) for k, v in dd.items()}
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
            'teacher': prettify_teacher(teacher),
            'links': prettify_links(links),
        })

    subjects = convert_to_dict(subjects)
    # pprint(subjects)
    return subjects


def title_key(entry):
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


def subject_key(pair):
    subject = pair[0]
    if subject in ['ІМ', 'ІМ1п', 'ІМ2п', 'ФВ']:
        return 3, subject
    if subject.startswith('*'):
        return 2, subject
    return 1, subject


def prepare_entries(entries):
    subjects = create_dict(entries)
    subjects = dict(sorted(subjects.items(), key=subject_key))

    for subject, data in subjects.items():
        for category in data.keys():
            data[category] = list(sorted(data[category], key=title_key))

    return subjects
