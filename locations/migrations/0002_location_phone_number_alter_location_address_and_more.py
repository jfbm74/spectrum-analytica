# Generated by Django 4.2.2 on 2023-06-24 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='phone_number',
            field=models.CharField(default=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.CharField(default=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(default=True, max_length=200),
        ),
    ]