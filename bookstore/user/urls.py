from django.urls import path
from .views import RegistrationView, ActivationView, ResetViaEmailView, ResetPWView, LoginWithCheck
from django.views.generic import TemplateView
urlpatterns=[
    path('sign_up/', RegistrationView.as_view(),name='sign_up'),
    path('login/', LoginWithCheck.as_view(), name='login'),
    path('applied/', TemplateView.as_view(template_name="user/thanks.html"), name='thanks'),
    path('activate/<str:username>/<str:token>', ActivationView.as_view(), name='activation'),
    path('reset_me/', ResetViaEmailView.as_view(), name='reset_pw'),
    path('reset_me/<str:username>/<str:token>', ResetPWView.as_view(), name='reset_access_allowed'),
]