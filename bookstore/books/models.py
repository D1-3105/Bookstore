from django.db import models
from django.contrib.auth import user_logged_in

class Books(models.Model):
    authors=models.ManyToManyField("Authors", related_name= "books_BooksToAuthor")
    name=models.TextField()
    volume=models.BigIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    downloads=models.BigIntegerField()
    rate=models.DecimalField(max_digits=7, decimal_places=5, default=0)
    # reviews=models.ManyToManyField("Reviews2Books", related_name= "books_BooksToReviews")
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


class Reviews2Books(models.Model):
    review_text=models.TextField(default='')
    review_rate=models.SmallIntegerField()
    author= models.ForeignKey("user.CustomUser", on_delete=models.CASCADE)
    book=models.ForeignKey("books.Books", on_delete=models.CASCADE)

    class Meta:
        unique_together=['author', 'book']

# Create your models here.
