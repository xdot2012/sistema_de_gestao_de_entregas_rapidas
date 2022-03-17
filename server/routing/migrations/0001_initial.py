# Generated by Django 3.0.7 on 2022-03-16 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('legacy', '0012_auto_20220303_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, verbose_name='Endereço')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('altitude', models.FloatField(verbose_name='Altitude')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='legacy.Client')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]