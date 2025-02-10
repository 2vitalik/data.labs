from os.path import join

from django.conf import settings


def read_file(filename):
    filepath = join('data', settings.SEMESTER, filename)
    return open(filepath, encoding='utf-8').read().strip()
