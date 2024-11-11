from django.shortcuts import redirect
from django.views.generic import TemplateView

from src.entries_tree import prepare_entries
from utils.mongo_db import db


class IndexView(TemplateView):
    template_name = 'index.html'


class LinksBaseView(TemplateView):
    template_name = 'links.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        key = self.kwargs['key']
        semester, prefix = db.groups.get(key)
        subjects = prepare_entries(db.entries.get(semester, prefix))
        subjects_names = db.subjects.get(semester, prefix)
        context.update({
            'key': key,
            'semester': semester,
            'prefix': prefix,
            'subjects': subjects,
            'subjects_names': subjects_names,
        })
        return context


class LinksView(LinksBaseView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'mode': 'view',
        })
        return context


class LinksEditView(LinksBaseView):
    def post(self, request, *args, **kwargs):
        key = self.kwargs['key']
        semester, prefix = db.groups.get(key)
        db.entries.edit(semester, prefix, request.POST)
        return redirect('links', key=self.kwargs['key'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'mode': 'edit',
        })
        return context
