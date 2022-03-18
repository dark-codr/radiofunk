# Generated by Django 3.2.12 on 2022-03-18 13:20

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tunes', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stations',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank='True', editable=False, populate_from='name', unique='True', verbose_name='slug'),
        ),
    ]