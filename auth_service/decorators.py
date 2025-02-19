from functools import wraps
from django.http import HttpResponseForbidden

def role_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_student or request.user.is_teacher or request.user.is_manager:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return _wrapped_view

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_teacher or request.user.is_manager:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return _wrapped_view

def manager_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_manager:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return _wrapped_view