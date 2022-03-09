# Generated by Django 3.0.7 on 2022-02-21 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legacy', '0005_auto_20220218_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryMan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='Telefone')),
                ('vehycle_type', models.CharField(choices=[('CAR', 'Carro'), ('MOTORCYCLE', 'Moto'), ('BIKE', 'Bicicleta')], max_length=15, verbose_name='Tipo do Veículo')),
                ('status', models.CharField(choices=[('IDLE', 'Aguardando'), ('UNAVAILABLE', 'Indisponível'), ('IN_ROUTE', 'Em rota')], max_length=15, verbose_name='Situação')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]