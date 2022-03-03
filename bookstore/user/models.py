from django.contrib.auth.models import AbstractUser
from django.db.models import FloatField, ManyToManyField, BigIntegerField, TextField, BooleanField
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
import random


class CustomUser(AbstractUser):

    balance = FloatField(default=0)
    owned_books = ManyToManyField("books.Books", "users_Owned_Books", blank=True, default=0)
    reviews_sent = BigIntegerField(blank=True, null=True, default=0)
    wish_list = ManyToManyField("books.Books", "users_Wish_List", blank=True)
    token = TextField(blank= True)
    confirmed=BooleanField(default=False)

    def change_token(self):
        self.token=''
        len_token=random.randint(10,40)
        abc='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(len_token):
            self.token+=random.choice(abc)
        return self.token

    def send_token(self, url, type_ra='activate'):
        self.change_token()

        if type_ra=='activate':
            url+=("{}/{}".format(self.username, self.token))
            send_my_mail(self.email, 'user/activation.html', settings.SERVER_MAIL,
                        self.email, self.username, url)
        else:
            url+=("{}/{}".format(self.username, self.token))
            send_my_mail(self.email, 'user/reset_message.html', settings.SERVER_MAIL,
                         self.email, self.username, url)

    def __str__(self):
        return self.username + "-" + self.email

    def get_absolute_url(self):
        # here profile method
        pass

    def increment_balance(self, balance):
        self.balance += balance

    def decrement_balance(self, balance):
        self.balance -= balance


# Create your models here.


def send_my_mail(subject, template:str, from_, to, username, url):
    content={
        'username':username,
        'recover_link':url
    }
    html_part=render_to_string(template, content)
    send_mail(subject, '', from_, [to], html_message=html_part)