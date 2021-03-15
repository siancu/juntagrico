# Generated by Django 3.1.5 on 2021-01-17 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico', '0030_auto_20201112_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='cancellation_date',
            field=models.DateField(blank=True, null=True, verbose_name='Kündigungsdatum'),
        ),
        migrations.AddField(
            model_name='depot',
            name='depot_list',
            field=models.BooleanField(default=True, verbose_name='Sichtbar auf Depotliste'),
        ),
        migrations.AddField(
            model_name='depot',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='Sichtbar'),
        ),
        migrations.AlterField(
            model_name='depot',
            name='code',
            field=models.CharField(default='', max_length=100, unique=False, null=True),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='activityarea',
            options={'ordering': ['sort_order'], 'permissions': (('is_area_admin', 'Benutzer ist TätigkeitsbereichskoordinatorIn'),), 'verbose_name': 'Tätigkeitsbereich', 'verbose_name_plural': 'Tätigkeitsbereiche'},
        ),
        migrations.AlterModelOptions(
            name='depot',
            options={'ordering': ['sort_order'], 'permissions': (('is_depot_admin', 'Benutzer ist Depot Admin'),), 'verbose_name': 'Depot', 'verbose_name_plural': 'Depots'},
        ),
        migrations.AlterModelOptions(
            name='extrasubscriptioncategory',
            options={'ordering': ['sort_order'], 'verbose_name': 'Zusatz-Abo-Kategorie', 'verbose_name_plural': 'Zusatz-Abo-Kategorien'},
        ),
        migrations.AlterModelOptions(
            name='extrasubscriptiontype',
            options={'ordering': ['sort_order'], 'verbose_name': 'Zusatz-Abo-Typ', 'verbose_name_plural': 'Zusatz-Abo-Typen'},
        ),
        migrations.AlterModelOptions(
            name='listmessage',
            options={'ordering': ['sort_order'], 'verbose_name': 'Depot Listen Nachricht', 'verbose_name_plural': 'Depot Listen Nachrichten'},
        ),
        migrations.AlterModelOptions(
            name='subscriptionproduct',
            options={'ordering': ['sort_order'], 'verbose_name': 'Abo-Produkt', 'verbose_name_plural': 'Abo-Produkt'},
        ),
        migrations.AlterModelOptions(
            name='subscriptiontype',
            options={'ordering': ['sort_order'], 'verbose_name': 'Abo-Typ', 'verbose_name_plural': 'Abo-Typen'},
        ),
        migrations.AddField(
            model_name='depot',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Reihenfolge'),
        ),
        migrations.AddField(
            model_name='activityarea',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Reihenfolge'),
        ),
        migrations.AddField(
            model_name='subscriptionproduct',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Reihenfolge'),
        ),
        migrations.AddField(
            model_name='subscriptiontype',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Reihenfolge'),
        ),
        migrations.AlterField(
            model_name='extrasubscriptioncategory',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Reihenfolge'),
        ),
        migrations.AlterField(
            model_name='extrasubscriptiontype',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Reihenfolge'),
        ),
        migrations.AlterField(
            model_name='listmessage',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Reihenfolge'),
        ),
        migrations.AlterModelOptions(
            name='specialroles',
            options={'permissions': (
            ('is_operations_group', 'Benutzer ist in der BG'), ('is_book_keeper', 'Benutzer ist Buchhalter'),
            ('can_send_mails', 'Benutzer kann im System Emails versenden'),
            ('can_use_general_email', 'Benutzer kann General Email Adresse verwenden'),
            ('depot_list_notification', 'Benutzer wird bei Depot-Listen-Erstellung informiert'))},
        ),
    ]