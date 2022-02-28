from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUserModel:
    User=get_user_model()
    def set_up(self):
        self.User=self.User.objects.create_user(
            username='john',
            email='lyerhd@gmail.com',
            password='password111',
            balance=1,

        )

# Create your tests here.
