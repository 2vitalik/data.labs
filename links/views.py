from django.views.generic import TemplateView

from src.entries_tree import prepare_entries
from utils.mongo_db import db


class IndexView(TemplateView):
    template_name = 'index.html'


class LinksView(TemplateView):
    template_name = 'links.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        semester, prefix = db.groups.get(self.kwargs['key'])
        subjects = prepare_entries(db.entries.get(semester, prefix))
        subjects_names = db.subjects.get(semester, prefix)
        context.update({
            'semester': semester,
            'prefix': prefix,
            'subjects': subjects,
            'subjects_names': subjects_names,
        })
        return context
