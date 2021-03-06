from django.urls import path
from .views import MainView, BookPageView, BookBuyView, WishAppendView, AuthorView, SearchView
from django.contrib.auth.decorators import login_required
urlpatterns=[
    path('', MainView.as_view(), name='main_page'),
    path('page/<int:page>', MainView.as_view(), name='main_with_num'),
    path('book/id<int:pk>', BookPageView.as_view(), name='book_page'),
    path('book/id<int:pk>/buy', login_required(BookBuyView.as_view()), name='book_buy'),
    path('book/id<int:pk>/wish_list', login_required(WishAppendView.as_view()), name='book_wished'),
    path('author/id<int:pk>', AuthorView.as_view(), name='author'),
    path('search/', SearchView.as_view(), name='search_init'),
    path('search/<int:num>', SearchView.as_view(), name='search_with_page')
]
