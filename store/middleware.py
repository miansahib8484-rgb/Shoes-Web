from django.shortcuts import redirect
from django.contrib.auth import logout

class AdminAccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            user = request.user

          
            if not user.is_authenticated or not user.is_staff:
                logout(request)
                return redirect('/')

           
            if hasattr(user, 'userprofile') and not user.userprofile.can_access_admin:
                logout(request)
                return redirect('/')

        return self.get_response(request)
