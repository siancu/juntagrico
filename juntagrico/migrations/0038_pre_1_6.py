# Generated by Django 4.0.1 on 2022-02-08 21:42

import django.db.models.deletion
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico', '0037_post_1_5'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='specialroles',
            options={'default_permissions': (), 'managed': False, 'permissions': (
                ('is_operations_group', 'Benutzer ist in der BG'), ('is_book_keeper', 'Benutzer ist Buchhalter'), ('can_send_mails', 'Benutzer kann im System E-Mails versenden'),
                ('can_use_general_email', 'Benutzer kann allgemeine E-Mail-Adresse verwenden'), ('can_use_for_members_email', 'Benutzer kann E-Mail-Adresse "for_members" verwenden'),
                ('can_use_for_subscriptions_email', 'Benutzer kann E-Mail-Adresse "for_subscription" verwenden'), ('can_use_for_shares_email', 'Benutzer kann E-Mail-Adresse "for_shares" verwenden'),
                ('can_use_technical_email', 'Benutzer kann technische E-Mail-Adresse verwenden'), ('depot_list_notification', 'Benutzer wird bei Depot-Listen-Erstellung informiert'),
                ('can_view_exports', 'Benutzer kann Exporte öffnen'), ('can_view_lists', 'Benutzer kann Listen öffnen'), ('can_generate_lists', 'Benutzer kann Listen erzeugen')
            )},
        ),
        migrations.AlterField(
            model_name='subscriptionmembership',
            name='join_date',
            field=models.DateField(blank=True, help_text='Erster Tag an dem Abo bezogen wird', null=True, verbose_name='Beitrittsdatum'),
        ),
        migrations.AlterField(
            model_name='subscriptionmembership',
            name='leave_date',
            field=models.DateField(blank=True, help_text='Letzter Tag an dem Abo bezogen wird', null=True, verbose_name='Austrittsdatum'),
        ),
        migrations.AlterField(
            model_name='subscriptionmembership',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='juntagrico.member', verbose_name='Mitglied'),
        ),
        migrations.AlterField(
            model_name='subscriptionmembership',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='juntagrico.subscription', verbose_name='Abo'),
        ),
        migrations.AlterField(
            model_name='job',
            name='multiplier',
            field=models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Arbeitseinsatz vielfaches'),
        ),
        migrations.AlterField(
            model_name='share',
            name='reason_for_acquisition',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Gründungsmitglied'), (2, 'Beitrittserklärung'), (3, 'Beitritts- und Übertragungserklärung'), (4, 'Übertragungserklärung'),
                                                                   (5, 'Erhöhung der Anteile'), (6, 'Betriebsbeteiligung - Lohn')], null=True, verbose_name='Grund des Erwerbs'),
        ),
        migrations.AlterModelOptions(
            name='subscription',
            options={'permissions': [('can_filter_subscriptions', 'Benutzer kann Abo filtern'),
                                     ('can_change_deactivated_subscriptions', 'Benutzer kann deaktivierte Abo ändern'),
                                     ('notified_on_depot_change', 'Wird bei Depot-Änderung informiert'),
                                     ('notified_on_subscription_creation', 'Wird bei Abo Erstellung informiert'),
                                     ('notified_on_subscription_cancellation', 'Wird bei Abo Kündigung informiert')],
                     'verbose_name': 'Abo', 'verbose_name_plural': 'Abos'},
        ),
    ]