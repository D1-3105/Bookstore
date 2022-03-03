from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import View, FormView, TemplateView
from .forms import CustomUserCreationForm, ResetEmailForm, CustomUserChangeForm
from django.contrib.auth import get_user_model, mixins
from django.contrib.auth.views import LoginView
from django.db.models import Q
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
stripe.api_key=settings.STRIPE_SEC_KEY

class RegistrationView(View):
    template_name = 'user/sign_up.html'
    form_class = CustomUserCreationForm

    def get(self, request, **kwargs):
        context = {
            'form': self.form_class,
            'title': "Sign Up!"
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.send_token(url="{}".format(request.build_absolute_uri('/accounts/activate/')), )
            obj.save()
            return redirect(reverse("thanks"))
        redirect(reverse("404"))


class ActivationView(View):

    def get(self, request, **kwargs):
        tok = kwargs['token']
        un = kwargs['username']
        try:
            user = get_user_model().objects.filter(Q(username=un) | Q(token=tok)).get()
            user.confirmed = True
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
        user_name = request.POST.dict()['username']
        try:
            user = get_user_model().objects.get_by_natural_key(user_name)
            if user.confirmed:
                pass
            else:
                return render(request, "user/check_box.html")
        except:
            # means there is no such user.
            return redirect(reverse("404"))
        return super(LoginWithCheck, self).post(request, *args, **kwargs)


class ProfileView(View, mixins.LoginRequiredMixin):
    login_url = reverse_lazy('login')
    template_name = 'user/profile.html'

    def get(self, request, **kwargs):
        authed = request.user.pk is kwargs['pk']
        context = {}
        if authed:
            context['authed'] = 1
            context['user1'] = request.user
        else:
            context['user1'] = get_user_model().objects.get(pk=kwargs['pk'])
        return render(request, self.template_name, context=context)


class BalanceView(TemplateView, mixins.LoginRequiredMixin):
    login_url = reverse_lazy('login')
    template_name = 'user/balance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_key'] = settings.STRIPE_PUB_KEY
        return context


@login_required
def charge(request):
    if request.POST:
        charge_stripe = stripe.Charge.create(
            amount=int(request.POST['amount_get']) * 100,
            currency='usd',
            description='Charge for bookstore',
            source=request.POST['stripeToken']
        )
        request.user.increment_balance(float(request.POST['amount_get']))
        request.user.save()
        return render(request, "user/charge.html")
