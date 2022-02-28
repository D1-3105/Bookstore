# Generated by Django 4.0.2 on 2022-02-28 22:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0005_alter_books_rate_reviews2books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='rate',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=7),
        ),
        migrations.AlterUniqueTogether(
            name='reviews2books',
            unique_together={('author', 'book')},
        ),
    ]