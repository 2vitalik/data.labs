from django.views.generic import TemplateView

from utils.mongo_db import db


class IndexView(TemplateView):
    template_name = 'index.html'


class GroupView(TemplateView):
    template_name = 'group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        key = self.kwargs['key']
        group = db.groups.get_group(key)
        context.update({
            'group': group,
        })
        return context
