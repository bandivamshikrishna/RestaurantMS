# Generated by Django 4.0.3 on 2022-05-14 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0016_foodorder_checked_alter_foodorder_food_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodorder',
            name='food_quantity',
            field=models.CharField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (10, 10), (20, 20)], default=1, max_length=40),
        ),
    ]
