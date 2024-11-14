from django.shortcuts import redirect
from django.views.generic import TemplateView

from src.entries_tree import prepare_entries
from src.track_user import get_user_args
from utils.mongo_db import db


class IndexView(TemplateView):
    template_name = 'index.html'


class LinksBaseView(TemplateView):
    template_name = 'links.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        key = self.kwargs['key']
        semester, prefix = db.groups.get(key)
        if prefix:
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
    def get_changes(self):
        changes = {}
        post = self.request.POST.copy()
        post.pop('csrfmiddlewaretoken')
        for key, value in post.items():
            if key.startswith('old|'):
                continue
            old_value = post.get('old|' + key)
            new_value = post.get(key)
            if old_value != new_value:
                changes[key] = new_value
        return changes

    def post(self, request, *args, **kwargs):
        key = self.kwargs['key']
        semester, prefix = db.groups.get(key)
        user_args = get_user_args(request)
        db.entries.edit(semester, prefix, self.get_changes(), user_args)
        return redirect('links', key=self.kwargs['key'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'mode': 'edit',
        })
        return context
