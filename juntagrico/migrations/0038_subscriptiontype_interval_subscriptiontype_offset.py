# Generated by Django 4.0.10 on 2023-03-19 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico', '0037_post_1_5'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptiontype',
            name='interval',
            field=models.PositiveIntegerField(default=1, verbose_name='Intervall'),
        ),
        migrations.AddField(
            model_name='subscriptiontype',
            name='offset',
            field=models.PositiveIntegerField(default=0, verbose_name='Versatz'),
        ),
    ]
