# Generated by Django 3.0.5 on 2020-05-05 20:12

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_item_video_vid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='video_vid',
        ),
        migrations.AddField(
            model_name='item',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True),
        ),
    ]
