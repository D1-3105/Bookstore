# Generated by Django 4.0.2 on 2022-02-27 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customuser_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='reviews_sent',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
