# Generated by Django 4.0.3 on 2022-05-11 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReserveTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seater', models.IntegerField()),
                ('table_pic', models.ImageField(blank=True, null=True, upload_to='table_pic/')),
            ],
        ),
    ]
