
def get_user_args(request):
    return {
        'csrf_token': request.COOKIES.get('csrftoken'),
        'user_ip': request.META.get('REMOTE_ADDR'),
        'user_agent': request.META.get('HTTP_USER_AGENT'),
    }
