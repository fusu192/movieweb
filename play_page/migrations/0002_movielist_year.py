# Generated by Django 2.2.5 on 2020-10-11 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play_page', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movielist',
            name='year',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
    ]
