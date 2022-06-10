# Generated by Django 4.0.3 on 2022-05-31 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0034_remove_tableorder_customer_tableorder_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tableorder',
            name='customer',
        ),
        migrations.AddField(
            model_name='tableorder',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customer'),
        ),
    ]
