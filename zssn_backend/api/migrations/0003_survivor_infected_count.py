# Generated by Django 3.2.25 on 2024-07-18 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_inventory_survivor'),
    ]

    operations = [
        migrations.AddField(
            model_name='survivor',
            name='infected_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]