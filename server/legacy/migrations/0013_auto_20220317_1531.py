# Generated by Django 3.0.7 on 2022-03-17 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legacy', '0012_auto_20220303_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=16, max_digits=22, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=16, max_digits=22, null=True)),
            ],
            options={
                'unique_together': {('latitude', 'longitude')},
            },
        ),
        migrations.DeleteModel(
            name='Local',
        ),
    ]
