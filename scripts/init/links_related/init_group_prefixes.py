import utils.django_bin

from mongo.db import db
from scripts.init.links_related.src.read_texts import read_groups_splits


def init_group_prefixes():
    groups_splits = read_groups_splits()

    print('Prefixes:')
    for prefix, (split, total) in groups_splits.items():
        print(f'- Prefix: "{prefix}" ({split}|{total})')
        if not db.group_prefixes.exists(prefix):
            db.group_prefixes.add(prefix, split, total)
            print('  [+] Added')
        else:
            print('  [-] Already exists')


if __name__ == '__main__':
    init_group_prefixes()
