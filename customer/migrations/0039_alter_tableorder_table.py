# Generated by Django 4.0.3 on 2022-06-03 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_reservefood_food_type'),
        ('customer', '0038_remove_tableorder_customer_tableorder_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tableorder',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.reservetable'),
        ),
    ]
