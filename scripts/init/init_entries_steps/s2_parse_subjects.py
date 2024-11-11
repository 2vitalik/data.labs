import re
from collections import defaultdict
from pprint import pprint


def parse_subjects(prefix, subjects_text):
    subjects = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

    for subject_line in subjects_text.split('\n'):
        m = re.fullmatch(r'(?P<short>[^\t]+)\t(?P<long>.+) : '
                         r'(?P<subject_data>.*)', subject_line)
        if not m:
            raise Exception(f'Wrong `subject_line` format: "{subject_line}"')

        short, long, subject_data = m.groups()
        if short in ['ФВ']:
            continue  # skip because no teachers there

        # print(f"{'=' * 100}\n{short} - {long}\n{'-' * 100}")

        for part in subject_data.split(':'):
            part = part.strip()
            if not part:
                continue

            process_part(subjects, prefix, short, long, part)

    # pprint(subjects)
    return subjects


def process_part(subjects, prefix, short, long, part):

    m = re.fullmatch(r'(?P<kind>Лк|Пз|Лб|Конс|Екз|Зал) '
                     r'\(\d+\) - '
                     r'(?P<groups>.+?), '
                     r'(?P<teachers>.*)',
                     part)
    if not m:
        raise Exception(f'Wrong `part` format: "{part}"')

    kind, groups, teachers = m.groups()
    if kind in ['Екз', 'Зал', 'Конс', ]:
        return
    if kind not in ['Лк', 'Пз', 'Лб', ]:
        raise Exception(f'Wrong `kind`: "{kind}"')

    is_alternative = (
        short.startswith('*') and '*' in groups and '(' in groups
        or
        long.startswith('*') and '(' in groups
    )

    if is_alternative:
        groups = {0}

    else:
        # Replace `ПЗПІ-24-1` to `1` (etc.)
        groups = re.sub(f'{prefix}-', '', groups)

        # Remove other groups (e.g. not `ПЗПІ-24-X`)
        groups = re.sub('[А-ЯІЄа-яіє]+-\d\d-\d\d?', '', groups)

        # Create a list of numbers
        groups = re.split('[,;]', groups)

        # Remove empty strings
        groups = set(filter(None, groups))

        # Convert elements to int
        groups = set(map(int, groups))

        if not groups:  # if all groups are not ours completely
            return

    # Remove `initials`, leave only `surname`:
    # teachers = re.sub(' [А-ЯІЄ0]\. [А-ЯІЄ0]\.', '', teachers)

    # Remove surname duplicates:
    teachers = ', '.join(set(teachers.split(', ')))

    # print(teachers, kind, groups)
    subjects[short][teachers][kind].update(groups)
