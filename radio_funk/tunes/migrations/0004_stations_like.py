# Generated by Django 3.2.11 on 2022-03-12 02:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tunes', '0003_alter_stations_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='stations',
            name='like',
            field=models.ManyToManyField(blank=True, default=None, related_name='radio_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]