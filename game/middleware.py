from django.http import HttpResponseForbidden
from django.core.cache import cache
from .models import BannedIP

class BannedIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        if ip:
            if BannedIP.objects.filter(ip_address=ip).exists():
                return HttpResponseForbidden("Ваш IP-адрес заблокирован Администратором сервера.")

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
