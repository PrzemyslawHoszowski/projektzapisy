# Generated by Django 3.1.5 on 2021-01-30 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0034_auto_20201106_2039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='order',
        ),
        migrations.AlterField(
            model_name='classroom',
            name='usos_id',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='ID sali w systemie USOS'),
        ),
        migrations.AlterField(
            model_name='group',
            name='usos_nr',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nr grupy w usos'),
        ),
    ]