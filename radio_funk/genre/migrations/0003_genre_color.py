# Generated by Django 3.2.11 on 2022-03-14 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genre', '0002_auto_20220311_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='color',
            field=models.CharField(blank=True, max_length=10, verbose_name='Background Color'),
        ),
    ]