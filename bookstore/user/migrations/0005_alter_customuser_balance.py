# Generated by Django 4.0.3 on 2022-03-03 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_customuser_confirmed_customuser_token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='balance',
            field=models.FloatField(),
        ),
    ]