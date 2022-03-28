# Generated by Django 3.2.12 on 2022-03-28 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routing', '0001_initial'),
        ('legacy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='routing.clientaddress', verbose_name='Endereço'),
            preserve_default=False,
        ),
    ]
