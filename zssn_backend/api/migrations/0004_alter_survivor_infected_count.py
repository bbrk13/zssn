# Generated by Django 3.2.25 on 2024-07-20 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_survivor_infected_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survivor',
            name='infected_count',
            field=models.IntegerField(default=0),
        ),
    ]
