# Generated by Django 3.2.12 on 2022-05-24 12:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('legacy', '0009_auto_20220520_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='Telefone'),
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together={('phone', 'created_by')},
        ),
    ]