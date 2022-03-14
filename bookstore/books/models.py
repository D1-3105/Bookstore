from django.db import models




class Books(models.Model):
    authors=models.ManyToManyField("Authors", related_name= "books_BooksToAuthor", blank=True)
    name=models.TextField()
    volume=models.BigIntegerField()
    price=models.FloatField()
    downloads=models.BigIntegerField()
    rate=models.FloatField(default=0)
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
    rate=models.FloatField(default=0)
    name=models.TextField(default='')
    bio= models.TextField(blank=True)

    def get_absolute_url(self):
        # here is author_page
        pass

    def __str__(self):
        return self.name


class ReviewsManager(models.Manager):

    def create_review_author(self, review, author):
        try:# try to find review
            review_prev=Reviews2Authors.objects.filter(author=author,
                                                       reviewer=review.reviewer).get()# prev review
            rev_count=Reviews2Authors.objects.filter(author=author).count()
            author.rate=author.rate-float(review_prev.review_rate)/rev_count+float(review.review_rate)/rev_count
            review_prev.review_rate=review.review_rate
            review_prev.review_text=review.review_text
            review=review_prev
        except models.ObjectDoesNotExist:
            rev_count = Reviews2Authors.objects.filter(author=author).count()
            author.rate = (author.rate + float(review.review_rate)) / (rev_count+1)# +1 because review is not created!
        finally:
            review.save()
            author.save()


    def create_review_book(self, review, book):
        try:  # try to find review
            review_prev = Reviews2Books.objects.filter(book=book,
                                                       author=review.author).get()  # prev review
            rev_count = Reviews2Books.objects.filter(book=book).count()
            book.rate = book.rate - float(review_prev.review_rate) / rev_count + float(
                review.review_rate) / rev_count
            review_prev.review_rate = review.review_rate
            review_prev.review_text = review.review_text
            review = review_prev
        except models.ObjectDoesNotExist:
            rev_count = Reviews2Books.objects.filter(book=book).count()
            book.rate = (book.rate + float(review.review_rate)) / (rev_count + 1)  # +1 because review is not created!
        finally:
            review.save()
            book.save()


class Reviews2Books(models.Model):
    review_text=models.TextField(default='')
    review_rate=models.SmallIntegerField()
    author= models.ForeignKey("user.CustomUser", on_delete=models.CASCADE) # reviewer!!
    book=models.ForeignKey("books.Books", on_delete=models.CASCADE)
    objects= ReviewsManager()

    class Meta:
        unique_together=['author', 'book']


class Reviews2Authors(models.Model):
    review_text=models.TextField(default='')
    review_rate=models.SmallIntegerField()
    reviewer= models.ForeignKey("user.CustomUser", on_delete=models.CASCADE)
    author = models.ForeignKey("books.Authors", on_delete=models.CASCADE) # author of book!
    objects=ReviewsManager()
    class Meta:
        unique_together=['reviewer', 'author']

