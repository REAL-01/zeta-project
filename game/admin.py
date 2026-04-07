from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Player, BannedIP

class PlayerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Игровые данные', {'fields': ('role', 'playerGold', 'playerXp', 'currentRankIdx', 'lightbulbs', 'researchedTechs', 'games_played')}),
    )
    list_display = ('username', 'email', 'role', 'games_played', 'playerGold', 'playerXp')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

@admin.register(BannedIP)
class BannedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'reason', 'created_at')
    search_fields = ('ip_address',)

admin.site.register(Player, PlayerAdmin)
