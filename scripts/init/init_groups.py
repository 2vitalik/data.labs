import utils.django_bin
from mongo.db import db


def init_groups():
    prefixes = [
        'ПЗПІ-24',
        'ПЗПІ-23',
        'ПЗПІ-22',
        'ПЗПІ-21',
        'ІПЗм-24',
        'ІПЗм-23',
    ]
    for prefix in prefixes:
        db.groups.add(prefix)


if __name__ == '__main__':
    init_groups()
