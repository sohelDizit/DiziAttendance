# Generated by Django 4.0.1 on 2023-01-08 06:37

import chat.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IP', models.CharField(max_length=200, verbose_name='IP')),
                ('Port', models.IntegerField(verbose_name='Port')),
                ('DeviceType', models.CharField(choices=[('1', 'IN'), ('2', 'OUT')], default='1', max_length=6, verbose_name='DeviceType')),
                ('Timeout', models.IntegerField(default=5, verbose_name='Timeout')),
                ('Password', models.CharField(default='0', max_length=200, verbose_name='Password')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EntryTime', models.DateTimeField(verbose_name='Entry Time')),
                ('ExitTime', models.DateTimeField(blank=True, null=True, verbose_name='Exit Time')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(blank=True, null=True, upload_to=chat.models.user_directory_path)),
                ('Name', models.CharField(max_length=200, verbose_name='Name')),
                ('MemberNumber', models.CharField(max_length=200, verbose_name='Member Number')),
                ('organisation', models.CharField(max_length=200, verbose_name='Organisation')),
                ('Details', models.TextField(blank=True, max_length=500, verbose_name='Details')),
                ('StartDate', models.DateField(null=True, verbose_name='Starting time')),
                ('Categorys', models.ManyToManyField(to='chat.Category', verbose_name="Category's")),
            ],
        ),
        migrations.CreateModel(
            name='GuestEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200, verbose_name='Name')),
                ('EntryTime', models.DateTimeField(null=True, verbose_name='Entry Time')),
                ('IdChecked', models.BooleanField()),
                ('ExitTime', models.DateTimeField(blank=True, null=True, verbose_name='Exit Time')),
                ('Entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.entry')),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='Customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.person'),
        ),
        migrations.AddField(
            model_name='entry',
            name='GuestEntrys',
            field=models.ManyToManyField(to='chat.GuestEntry'),
        ),
        migrations.CreateModel(
            name='CardNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CardNumber', models.CharField(max_length=200, verbose_name='Card Number')),
                ('Person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.person')),
            ],
        ),
    ]
