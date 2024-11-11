from datetime import datetime
from pprint import pprint

from django.conf import settings

from utils.mongo_db import db


def join_similar_entries(subject_data):
    all_kinds = tuple(sorted(  # e.g. ('Лб', 'Лк', 'Пз')
        set(kind
            for teacher_data in subject_data.values()
            for kind in teacher_data.keys())
    ))

    for teacher, teacher_data in subject_data.items():
        # check if:
        # - all values of dict are equal
        # - used all kinds of lessons for this subject
        # - there are several entries at least
        # - there is only one teacher
        if len(set(map(tuple, teacher_data.values()))) == 1 and \
                tuple(sorted(teacher_data.keys())) == all_kinds and \
                len(teacher_data) > 1 and len(subject_data) == 1:
            subject_data[teacher] = {'*': list(teacher_data.values())[0]}

        if teacher_data.get('Пз', {'~1'}) == teacher_data.get('Лб', {'~2'}):
            # default '~1' and '~2' are intentionally different and non-existent
            teacher_data['Пз,Лб'] = teacher_data['Пз']
            del teacher_data['Пз']
            del teacher_data['Лб']

    return subject_data


def compress_sequence(nums: str) -> str:
    nums = list(map(int, nums.split(',')))
    nums.append(float('inf'))  # Додаємо нескінченність як маркер кінця
    result = []

    start = end = nums[0]
    for i in range(1, len(nums)):
        if nums[i] == end + 1:
            end = nums[i]
        else:
            if end - start >= 2:
                result.append(f"{start}-{end}")
            elif start == end:
                result.append(f"{start}")
            else:
                result.append(f"{start},{end}")
            start = end = nums[i]

    return ','.join(result)


def get_prettified_title(kind, groups, case_all):
    if kind == '*':
        return 'Загальне'

    if kind == 'Лк':
        return f'Лекції'

    kind = kind.upper()
    groups = compress_sequence(groups)
    if groups == case_all:
        return f'{kind}'
    else:
        return f'{kind} ({groups} гр.)'


def entry(prefix, category, subject, title, teacher='', kind='*', groups='*'):
    return {
        'semester': settings.SEMESTER,
        'prefix': prefix,
        'category': category,
        'subject': subject,
        'title': title,
        'teacher': teacher,
        'kind': kind,  # not used, incorporated in `title`
        'groups': groups,  # not used, incorporated in `title`
        'links': '',
        'created_at': datetime.now(),
    }


def create_entries(prefix, subjects, category, case_all, groups_filter):
    print()
    print(prefix, category)
    entries = []

    for subject, subject_data in subjects.items():
        subject_data = join_similar_entries(subject_data)

        added = 0

        for teacher, teacher_data in subject_data.items():
            for kind, groups in teacher_data.items():
                groups = sorted(filter(groups_filter, groups))
                groups = ','.join(map(str, groups))
                if not groups:
                    continue
                title = get_prettified_title(kind, groups, case_all)
                args = (prefix, category, subject, title, teacher, kind, groups)
                print(*args)
                entries.append(entry(*args))
                added += 1

        if added > 1:
            args = (prefix, category, subject, 'Загальне')
            print(*args)
            entries.append(entry(*args))

    if entries:
        db.entries.add_many(entries)
