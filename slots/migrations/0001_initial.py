# Generated by Django 3.2.2 on 2021-05-15 06:43

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('district_name', models.CharField(max_length=64)),
                ('district_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('state_name', models.CharField(max_length=50)),
                ('state_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='slotrequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('pin', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('verify_mail_sent', models.CharField(default='NO', max_length=10)),
                ('processed', models.CharField(default='NO', max_length=10)),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='slots.district')),
                ('state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='slots.state')),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slots.state'),
        ),
    ]
