# Generated by Django 4.0 on 2021-12-29 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authcompleted',
            name='certificate_serial',
            field=models.CharField(auto_created=True, max_length=40, unique=True),
        ),
    ]
