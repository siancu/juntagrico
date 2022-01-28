# Generated by Django 4.0.1 on 2022-01-18 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico', '0039_alter_contact_sort_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='object_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='contact',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Reihenfolge'),
        ),
    ]