# Generated by Django 4.0.1 on 2023-01-29 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_person_relation'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='Max_guest_allowed',
            field=models.IntegerField(default=4, verbose_name='Maximum Guest Allowed'),
        ),
    ]
