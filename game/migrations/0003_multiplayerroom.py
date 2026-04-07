
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_player_enemies_destroyed_player_losses_player_wins'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultiplayerRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('waiting', 'Ожидание'), ('playing', 'В игре'), ('finished', 'Завершена')], default='waiting', max_length=20)),
                ('current_turn', models.CharField(default='host', max_length=10)),
                ('game_data', models.TextField(blank=True, default='{}')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('guest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='joined_rooms', to=settings.AUTH_USER_MODEL)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hosted_rooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
