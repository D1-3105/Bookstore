# Generated by Django 4.0.2 on 2022-02-28 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_authors_published_books'),
        ('user', '0003_alter_customuser_reviews_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='token',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='owned_books',
            field=models.ManyToManyField(blank=True, default=0, related_name='users_Owned_Books', to='books.Books'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='reviews_sent',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]
