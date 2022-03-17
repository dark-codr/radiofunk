# Generated by Django 3.2.11 on 2022-03-15 13:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('genre', '0003_genre_color'),
        ('podcast', '0005_auto_20220311_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episodes',
            name='keywords',
            field=models.ManyToManyField(blank=True, help_text='Select multiple genre from the list of predefined genres', related_name='episode', to='genre.Genre'),
        ),
        migrations.AlterField(
            model_name='episodes',
            name='published',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='published'),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='podcast', to='genre.Genre'),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='published',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True, verbose_name='published'),
        ),
    ]