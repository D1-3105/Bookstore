from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import CharField, TextInput, EmailInput, PasswordInput, \
    Form, EmailField


class CustomUserCreationForm(UserCreationForm):
    username = CharField(
        widget=TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    email = CharField(
        widget=EmailInput(attrs={
            'type': 'email',
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )

    password1 = CharField(
        widget=PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password2 = CharField(
        widget=PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )
    class Meta:
        model= get_user_model()
        fields=['email', 'username', 'password1', 'password2']


class ResetEmailForm(Form):
    username=CharField()
    email=EmailField()
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
    def is_valid(self):
        if self.Meta.model.objects.get_by_natural_key(username=self.data['username']).email==self.data['email'] \
                and self.data['email']!=None:
            return super().is_valid()
        return False


class CustomUserChangeForm(UserChangeForm):
    password = CharField()
    confirm=CharField()
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields= ('password', 'confirm')

    def is_valid(self):
        if self.data['password'] == self.data['confirm']:
            return super().is_valid()
        return False
