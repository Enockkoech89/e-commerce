# Generated by Django 3.0.5 on 2020-05-05 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='video_vid',
            field=models.FileField(blank=True, default='default.mp4', null=True, upload_to='vids'),
        ),
    ]