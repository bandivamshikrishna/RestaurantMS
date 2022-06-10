# Generated by Django 4.0.3 on 2022-05-12 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_customer_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.tableorder'),
        ),
        migrations.AlterField(
            model_name='tableorder',
            name='guests',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=1),
        ),
    ]
