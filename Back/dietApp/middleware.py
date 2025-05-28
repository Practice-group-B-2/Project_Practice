from django.http import HttpResponseForbidden

ALLOWED_IPS = ['127.0.0.1', '192.168.0.145']  # Add your IP addresses here

class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            ip = request.META.get('REMOTE_ADDR')
            if ip not in ALLOWED_IPS:
                return HttpResponseForbidden("Access denied. Your IP is not allowed.")
        response = self.get_response(request)
        return response 