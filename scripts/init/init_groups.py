import utils.django_bin
from utils.mongo_db import db


def init_groups():
    groups = [
        'ПЗПІ-24',
        'ПЗПІ-23',
        'ПЗПІ-22',
        'ПЗПІ-21',
        'ІПЗм-24',
        'ІПЗм-23',
    ]
    for group in groups:
        db.groups.add_group(group)


if __name__ == '__main__':
    init_groups()
