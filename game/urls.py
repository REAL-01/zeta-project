from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('play/', views.play_view, name='play'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('api/save/', views.api_save_game, name='api_save'),
    path('profile/', views.profile_view, name='profile'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('control_panel/', views.custom_admin_view, name='custom_admin'),
    path('lobby/', views.lobby_view, name='lobby'),
    path('api/mp/create/', views.api_mp_create, name='api_mp_create'),
    path('api/mp/join/<int:room_id>/', views.api_mp_join, name='api_mp_join'),
    path('api/mp/sync/<int:room_id>/', views.api_mp_sync, name='api_mp_sync'),
]
