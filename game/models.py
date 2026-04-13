from django.db import models
from django.contrib.auth.models import AbstractUser

class Player(AbstractUser):
    ROLE_CHOICES = (
        ('guest', 'Гость'),
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    playerGold = models.IntegerField(default=50, verbose_name="Ресурсы (Мета)")
    playerXp = models.IntegerField(default=0, verbose_name="Опыт")
    currentRankIdx = models.IntegerField(default=0, verbose_name="Ранг")
    lightbulbs = models.IntegerField(default=0, verbose_name="Лампочки")
    
    researchedTechs = models.TextField(default='', blank=True, verbose_name="Апгрейды")
    
    games_played = models.IntegerField(default=0, verbose_name="Сыграно боев")
    
    wins = models.IntegerField(default=0, verbose_name="Победы")
    losses = models.IntegerField(default=0, verbose_name="Поражения")
    enemies_destroyed = models.IntegerField(default=0, verbose_name="Уничтожено врагов")

    def __str__(self):
        return self.username


class BannedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True, verbose_name="IP Адрес")
    reason = models.CharField(max_length=255, blank=True, verbose_name="Причина бана")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Banned IP: {self.ip_address}"

class MultiplayerRoom(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'Ожидание'),
        ('playing', 'В игре'),
        ('finished', 'Завершена'),
    )

    host = models.ForeignKey(Player, related_name='hosted_rooms', on_delete=models.CASCADE)
    guest = models.ForeignKey(Player, related_name='joined_rooms', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    current_turn = models.CharField(max_length=10, default='host') # 'host' or 'guest'
    
    # Anti-cheat fields (Trusted state)
    host_gold_server = models.IntegerField(default=50)
    guest_gold_server = models.IntegerField(default=50)
    host_units_count = models.IntegerField(default=2)
    guest_units_count = models.IntegerField(default=2)
    
    game_data = models.TextField(default='{}', blank=True)
    game_version = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Room {self.id} ({self.host.username})"

