# Generated by Django 3.0.5 on 2020-05-20 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_auto_20200518_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='phone',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
    ]