# Generated by Django 4.0.3 on 2022-05-12 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_reservetable_seater'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservefood',
            name='food_type',
            field=models.CharField(choices=[('nonveg', 'NonVeg'), ('veg', 'Veg'), ('soups', 'Soups'), ('drinks', 'Drinks')], max_length=40, null=True),
        ),
    ]
