# Generated by Django 3.2.25 on 2024-07-22 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_delete_itemprices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survivor',
            name='infected_count',
        ),
    ]
