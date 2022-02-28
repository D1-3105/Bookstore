# Generated by Django 4.0.2 on 2022-02-27 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_rename_author_books_authors_authors_bio_authors_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='published_books',
            field=models.ManyToManyField(blank=True, null=True, related_query_name='books_AuthorPublished', to='books.Books'),
        ),
    ]