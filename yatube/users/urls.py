from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView

from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(template_name="registration/login.html"),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name="registration/logged_out.html"),
        name='logout'
    ),
    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name="registration/password_change_form.html"
        ),
        name='password_change'
    ),
    path('signup/', views.SignUp.as_view(), name='signup'),
]
