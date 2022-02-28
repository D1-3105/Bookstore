from django.urls import path
from .views import MainView
urlpatterns=[
    path('', MainView.as_view(), name='main_page'),
    path('page/<int:page>', MainView.as_view(), name='main_with_num')

]