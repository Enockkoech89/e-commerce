# Generated by Django 3.0.5 on 2020-05-18 18:12

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20200518_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('video', embed_video.fields.EmbedVideoField(blank=True)),
            ],
        ),
    ]
