from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    """
    Verificar si el usuario está autenticado (logged)
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
