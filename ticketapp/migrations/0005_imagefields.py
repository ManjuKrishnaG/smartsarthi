# Generated by Django 5.0.2 on 2024-04-30 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapp', '0004_pickuprequest_front'),
    ]

    operations = [
        migrations.CreateModel(
            name='imagefields',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='test/')),
            ],
        ),
    ]
