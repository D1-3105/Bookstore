# Generated by Django 4.0.3 on 2022-03-03 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_customuser_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]
