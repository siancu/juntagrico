# Generated by Django 3.1.5 on 2021-01-17 19:00

import django.db.models.deletion
from django.db import migrations, models

import juntagrico.entity.share


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
            model_name='subscriptionproduct',
            name='is_extra',
            field=models.BooleanField(default=False, verbose_name='Ist Zusatzabo Produkt'),
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
            options={'ordering': ['sort_order'],
                     'permissions': (('is_area_admin', 'Benutzer ist TätigkeitsbereichskoordinatorIn'),),
                     'verbose_name': 'Tätigkeitsbereich', 'verbose_name_plural': 'Tätigkeitsbereiche'},
        ),
        migrations.AlterModelOptions(
            name='depot',
            options={'ordering': ['sort_order'], 'permissions': (('is_depot_admin', 'Benutzer ist Depot Admin'),),
                     'verbose_name': 'Depot', 'verbose_name_plural': 'Depots'},
        ),
        migrations.AlterModelOptions(
            name='listmessage',
            options={'ordering': ['sort_order'], 'verbose_name': 'Depot Listen Nachricht',
                     'verbose_name_plural': 'Depot Listen Nachrichten'},
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
        migrations.AddField(
            model_name='share',
            name='value',
            field=models.DecimalField(decimal_places=2, default=juntagrico.entity.share.share_value_default, max_digits=8, verbose_name='Wert'),
        ),
        migrations.AddField(
            model_name='extrasubbillingperiod',
            name='type2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='periods2', to='juntagrico.subscriptiontype'),
        ),
        migrations.AddField(
            model_name='share',
            name='reason_for_acquisition',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Gründungsmitglied'), (2, 'Beitrittserklärung'),
                                                                   (3, 'Beitritts- und Übertragungserklärung')],
                                              null=True, verbose_name='Grund des Erwerbs'),
        ),
        migrations.AddField(
            model_name='share',
            name='reason_for_cancellation',
            field=models.PositiveIntegerField(blank=True,
                                              choices=[(1, 'Kündigung'), (2, 'Kündigung und Übertragungserklärung'),
                                                       (3, 'Ausschluss'), (4, 'Tod')], null=True,
                                              verbose_name='Grund der Kündigung'),
        ),
        migrations.AlterModelOptions(
            name='specialroles',
            options={'permissions': (('is_operations_group', 'Benutzer ist in der BG'), ('is_book_keeper', 'Benutzer ist Buchhalter'), ('can_send_mails', 'Benutzer kann im System Emails versenden'), ('can_use_general_email', 'Benutzer kann General Email Adresse verwenden'), ('depot_list_notification', 'Benutzer wird bei Depot-Listen-Erstellung informiert'), ('can_view_exports', 'Benutzer kann Exporte öffnen'), ('can_view_lists', 'Benutzer kann Listen öffnen'))},
        ),
        migrations.AlterField(
            model_name='jobtype',
            name='default_duration',
            field=models.FloatField(help_text='Standard-Dauer für diese Jobart', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Dauer in Stunden'),
        ),
        migrations.AlterField(
            model_name='onetimejob',
            name='default_duration',
            field=models.FloatField(help_text='Standard-Dauer für diese Jobart', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Dauer in Stunden'),
        ),
        migrations.AlterField(
            model_name='recuringjob',
            name='duration_override',
            field=models.FloatField(blank=True, default=None, help_text='Wenn nicht angegeben, wird die Standard-Dauer von der Jobart übernommen.', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Dauer in Stunden (Überschreibend)'),
        ),
    ]
