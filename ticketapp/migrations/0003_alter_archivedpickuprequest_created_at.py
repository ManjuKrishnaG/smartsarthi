# Generated by Django 5.0.2 on 2024-04-10 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapp', '0002_archivedpickuprequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivedpickuprequest',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
