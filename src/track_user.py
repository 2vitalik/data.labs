from functools import wraps

from utils.mongo_db import db


def get_user_args(request):
    return {
        'csrf_token': request.COOKIES.get('csrftoken'),
        'user_ip': request.META.get('REMOTE_ADDR'),
        'user_agent': request.META.get('HTTP_USER_AGENT'),
    }


def track_visit(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        full_path = request.get_full_path()
        db.visits.add(full_path, get_user_args(request))
        return view_func(request, *args, **kwargs)
    return _wrapped_view
