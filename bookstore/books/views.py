from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import View
from .models import Books, Reviews2Books, Authors, Reviews2Authors
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.conf import settings


class MainView(View):
    model = Books
    template_name = 'books/main_page.html'
    def getUser(self):
        if self.request.user.is_authenticated:
            return self.request.user
        else:
            return None

    def get(self, request, **kwargs):
        numpage=kwargs.get('page', 1)
        objects=[]
        for i in range(numpage*10-10,numpage*10):
            obj=''
            try:
                obj=Books.objects.get(pk=i)
            except:
                continue
            if obj.available and obj.published:
                objects.append(obj)
            else:
                pass
        prevAllowed=(numpage*10-11>0)#prev page
        nextAllowed=False#next page
        #next page
        try:
            nextObj=Books.objects.get(pk=numpage*10+1)
            nextAllowed=True
        except:
            #default
            pass

        context={
            'books': objects,
            'title': 'Books page {}'.format(numpage),
            'prev':(prevAllowed, numpage-1),
            'next':(nextAllowed, numpage+1),
        }
        return render(request, self.template_name, context=context)


class BookPageView(View):
    template_name= 'books/book_page.html'

    def post(self, request, **kwargs):
        req=request.POST
        book = Books.objects.get(pk=kwargs['pk'])
        print(req)
        if req.get('rating', None):
            # save review!
            review=Reviews2Books(
                author=request.user,
                book=book,
                review_rate=request.POST.get('rating', None),
                review_text=request.POST.get('review', '')
            )
            Reviews2Books.objects.create_review_book(review, book)
            return self.get(request, **kwargs)

        if req['download']:
            # send file!
            book = Books.objects.get(pk=kwargs['pk'])
            if book in request.user.owned_books.all():
                file_location = settings.BOOKS_DATA + book.path
                print(file_location)
                try:
                    with open(file_location, 'rb') as f:
                        file_data = f.read()
                    response = HttpResponse(file_data, headers={
                        'Content-Type': 'application/pdf',
                        'Content-Disposition': 'attachment; filename={}'.format(book.path),
                    })
                    return response
                except IOError:
                    return redirect(reverse('404'))


    def get(self, request, **kwargs):
        book = Books.objects.get(pk=kwargs['pk'])
        reviews = Reviews2Books.objects.filter(book=book).all()
        context={
            "book":book,
            "reviews":reviews
        }
        return render(request, self.template_name, context=context)


class BookBuyView(View, LoginRequiredMixin):
    login_url = reverse_lazy('login')

    def get(self, request, **kwargs):
        book=Books.objects.get(pk=kwargs['pk'])
        if request.user.balance>=book.price and book not in request.user.owned_books.all():
            print("OK")
            request.user.decrement_balance(book.price)
            request.user.owned_books.add(book)
            if book in request.user.wish_list.all():
                request.user.wish_list.remove(book)
            request.user.save()
        return redirect(reverse('book_page', args=str(kwargs['pk'])))


class WishAppendView(View, LoginRequiredMixin):
    login_url = reverse_lazy('login')

    def get(self, request, **kwargs):
        book=Books.objects.get(pk=kwargs['pk'])
        if book in request.user.wish_list.all():
            request.user.wish_list.remove(book)
        else:
            request.user.wish_list.add(book)
        return redirect(reverse('book_page', args=str(kwargs['pk'])))


class AuthorView(View):
    template_name="books/author_profile.html"

    def get(self, request, **kwargs):
        author=Authors.objects.get(pk=kwargs['pk'])
        print(author.published_books.all())
        reviews=""
        context = {
            'author': author,
        }
        try:
            reviews= Reviews2Authors.objects.filter(author=author).all()
            context['reviews']=reviews
        except:
            pass
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, **kwargs):
        author=Authors.objects.get(pk=kwargs['pk'])
        if request.POST.get('rating', None):
            print(request.POST.get('rating', None))
            review=Reviews2Authors(author=author, reviewer=request.user,
                                   review_rate=request.POST.get('rating', None),
                                   review_text=request.POST.get('review', ''))
            Reviews2Authors.objects.create_review_author(review, author)
            return self.get(request, **kwargs)
        else:
            return redirect(reverse('404'))