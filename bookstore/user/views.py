from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import View, FormView
from .forms import CustomUserCreationForm, ResetEmailForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.db.models import Q


class RegistrationView(View):
    template_name='user/sign_up.html'
    form_class=CustomUserCreationForm
    def get(self, request, **kwargs):
        context={
            'form':self.form_class,
            'title': "Sign Up!"
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        form=self.form_class(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.send_token(url="{}".format(request.build_absolute_uri('/accounts/activate/')), )
            obj.save()
            return redirect(reverse("thanks"))
        redirect(reverse("404"))


class ActivationView(View):

    def get(self, request, **kwargs):
        tok=kwargs['token']
        un=kwargs['username']
        try:
            user=get_user_model().objects.filter(Q(username=un)|Q(token=tok)).get()
            user.confirmed=True
            user.save()
        except:
            return redirect(reverse("404"))
        return redirect(reverse('login'))


class ResetViaEmailView(FormView):
    template_name = 'user/reset_via_email.html'
    form_class = ResetEmailForm
    success_url = reverse_lazy('thanks')

    def post(self, request, *args, **kwargs):
        old = request.POST.dict()
        user = get_user_model().objects.get_by_natural_key(username=old['username'])
        user.send_token(url=request.build_absolute_uri('/accounts/reset_me/'), type_ra='reset')
        return super().post(request, *args, **kwargs)


class ResetPWView(FormView):

    template_name = 'user/reset.html'
    success_url = reverse_lazy('thanks')
    form_class = CustomUserChangeForm

    def get(self, request, *args, **kwargs):
        un = kwargs['username']
        tok = kwargs['token']
        try:
            user = get_user_model().objects.get_by_natural_key(un)
            if user.token == tok:
                self.template_name = 'user/reset.html'
        except:
            self.template_name = '403.html'
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        un = kwargs['username']
        pw = request.POST.dict()['password']
        if self.get_form().is_valid():
            user = get_user_model().objects.get_by_natural_key(un)
            user.set_password(pw)
            user.change_token()
            user.save()
        return super().post(request, *args, **kwargs)


class LoginWithCheck(LoginView):
    def post(self, request, *args, **kwargs):
        user_name=request.POST.dict()['username']
        try:
            user=get_user_model().objects.get_by_natural_key(user_name)
            if user.confirmed:
                pass
            else:
                return render(request, "user/check_box.html")
        except:
            # means there is no such user.
            return redirect(reverse("404"))
        return super(LoginWithCheck, self).post(request, *args, **kwargs)
# Create your views here.
