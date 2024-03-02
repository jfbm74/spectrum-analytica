# Generated by Django 4.2.2 on 2023-06-24 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('name', models.CharField(max_length=1500)),
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]