from django.http import HttpResponseForbidden
from django.core.cache import cache
from .models import BannedIP

class BannedIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip:
            banned = cache.get('banned_ips')
            if banned is None:
                banned = set(BannedIP.objects.values_list('ip_address', flat=True))
                cache.set('banned_ips', banned, 60)
            
            if ip in banned:
                return HttpResponseForbidden("Ваш IP-адрес заблокирован Администратором сервера.")

        response = self.get_response(request)
        return response
