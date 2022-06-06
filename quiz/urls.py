"""medium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),

    # change password urls
    path('security/', auth_views.PasswordChangeView.as_view(template_name='security/password_change.html'), name='security'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='security/password_change_done.html'), 
        name='password_change_done'),

    # reset password urls
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='security/password_reset_done.html'),
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='security/password_reset_confirm.html'), 
        name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='security/password_reset_form.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='security/password_reset_complete.html'),
        name='password_reset_complete'),
]
