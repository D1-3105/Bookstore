# Generated by Django 4.0.2 on 2022-02-27 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='books',
            old_name='author',
            new_name='authors',
        ),
        migrations.AddField(
            model_name='authors',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='authors',
            name='name',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='books',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='books',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='authors',
            name='published_books',
            field=models.ManyToManyField(related_query_name='books_AuthorPublished', to='books.Books'),
        ),
    ]
