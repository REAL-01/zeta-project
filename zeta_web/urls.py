from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('hq-admin-zeta/', admin.site.urls),
    path('', include('game.urls')),
]
