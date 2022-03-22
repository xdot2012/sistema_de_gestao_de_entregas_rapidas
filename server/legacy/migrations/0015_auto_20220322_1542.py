# Generated by Django 3.2.12 on 2022-03-22 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legacy', '0014_auto_20220321_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='city_name',
        ),
        migrations.RemoveField(
            model_name='client',
            name='code',
        ),
        migrations.RemoveField(
            model_name='client',
            name='country_name',
        ),
        migrations.RemoveField(
            model_name='client',
            name='district',
        ),
        migrations.RemoveField(
            model_name='client',
            name='number',
        ),
        migrations.RemoveField(
            model_name='client',
            name='reference',
        ),
        migrations.RemoveField(
            model_name='client',
            name='state_name',
        ),
        migrations.RemoveField(
            model_name='client',
            name='street',
        ),
        migrations.CreateModel(
            name='ClientAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=100, verbose_name='País')),
                ('state_name', models.CharField(max_length=100, verbose_name='Estado')),
                ('city_name', models.CharField(max_length=100, verbose_name='Cidade')),
                ('number', models.PositiveIntegerField(verbose_name='Número')),
                ('street', models.CharField(max_length=100, verbose_name='Rua')),
                ('district', models.CharField(max_length=100, verbose_name='Bairro')),
                ('code', models.CharField(max_length=20, verbose_name='CEP')),
                ('reference', models.CharField(blank=True, max_length=200, null=True, verbose_name='Ponto de Referência')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='legacy.client')),
            ],
        ),
    ]
