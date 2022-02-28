from django.db import models


class Books(models.Model):
    authors=models.ManyToManyField("Authors", related_name= "books_BooksToAuthor")
    name=models.TextField()
    volume=models.BigIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    downloads=models.BigIntegerField()
    rate=models.DecimalField(max_digits=4, decimal_places=1)
    published=models.BooleanField(default=True)
    path=models.TextField(blank=True)
    available= models.BooleanField(default=True)
    bio=models.TextField(blank=True)

    def get_absolute_url(self):
        # here is book_page
        pass
    def __str__(self):
        return self.name


class Authors(models.Model):
    published_books=models.ManyToManyField("Books", related_query_name='books_AuthorPublished', blank=True)
    rate=models.DecimalField(max_digits=4, decimal_places=1)
    name=models.TextField(default='')
    bio= models.TextField(blank=True)

    def get_absolute_url(self):
        # here is author_page
        pass

    def __str__(self):
        return self.name



# Create your models here.
