# Generated by Django 2.2.5 on 2020-10-15 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play_page', '0009_auto_20201015_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='movielist',
            name='json_file',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
