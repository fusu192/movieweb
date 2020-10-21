# Generated by Django 2.2.5 on 2020-10-12 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play_page', '0004_auto_20201011_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='movielist',
            name='view_num',
            field=models.IntegerField(default=12, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movielist',
            name='star_num',
            field=models.CharField(max_length=1),
        ),
        migrations.AlterField(
            model_name='movielist',
            name='year',
            field=models.IntegerField(max_length=8),
        ),
    ]