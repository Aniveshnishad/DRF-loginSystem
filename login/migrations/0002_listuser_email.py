# Generated by Django 3.2.9 on 2021-12-02 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listuser',
            name='email',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]