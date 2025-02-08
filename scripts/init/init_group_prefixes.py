import utils.django_bin
from mongo.db import db


def init_group_prefixes():
    prefixes = [
        'ПЗПІ-24',
        'ПЗПІ-23',
        'ПЗПІ-22',
        'ПЗПІ-21',
        'ІПЗм-24',
        'ІПЗм-23',
    ]
    for prefix in prefixes:
        db.group_prefixes.add(prefix)


if __name__ == '__main__':
    init_group_prefixes()
