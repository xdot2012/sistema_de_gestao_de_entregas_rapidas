# Generated by Django 3.2.12 on 2022-05-19 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legacy', '0005_auto_20220518_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='appointment',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Horário de Entrega'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_type',
            field=models.CharField(choices=[('DEFAULT', 'Entrega Imediata'), ('PICKUP', 'Retirada no Local'), ('SCHEDULE', 'Agendar Horário')], max_length=20, verbose_name='Tipo de Entrega'),
        ),
        migrations.DeleteModel(
            name='OrderAppointment',
        ),
    ]