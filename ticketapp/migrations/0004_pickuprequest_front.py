# Generated by Django 5.0.2 on 2024-04-30 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapp', '0003_alter_archivedpickuprequest_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='pickuprequest',
            name='front',
            field=models.ImageField(blank=True, null=True, upload_to='attachments'),
        ),
    ]
