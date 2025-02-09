import utils.django_bin

from scripts.init.links_related.init_group_prefixes import init_group_prefixes
from scripts.init.links_related.init_links_entries import init_links_entries
from scripts.init.links_related.init_subjects import init_subjects


if __name__ == '__main__':
    init_group_prefixes()
    init_subjects()
    init_links_entries()
