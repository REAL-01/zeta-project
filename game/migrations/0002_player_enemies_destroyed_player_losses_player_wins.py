
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='enemies_destroyed',
            field=models.IntegerField(default=0, verbose_name='Уничтожено врагов'),
        ),
        migrations.AddField(
            model_name='player',
            name='losses',
            field=models.IntegerField(default=0, verbose_name='Поражения'),
        ),
        migrations.AddField(
            model_name='player',
            name='wins',
            field=models.IntegerField(default=0, verbose_name='Победы'),
        ),
    ]
