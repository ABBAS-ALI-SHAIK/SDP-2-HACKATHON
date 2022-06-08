from django.contrib.auth import logout
from django.shortcuts import redirect

def unauthenticate_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('userhome')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def access_roles(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff:
            logout(request)
            return redirect('userhome')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func