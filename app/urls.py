from msilib.schema import _Validation_records
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

from .views import QuizView, Register, SettingsView

urlpatterns = [
    path('', views.index, name="index"),
    path('@<str:username>', views.user_profile, name="profile"),
    path('quiz/<slug:slug>', QuizView.as_view(), name="quiz"),
    path('quiz/<slug:slug>/results', views.quiz_results, name="quiz_results"),
    path('quiz/<slug:slug>/check', views.check_results, name="check_results"),
    path('notifications', views.notifications, name="notifications"),
    path('notifications/delete/<int:id>', views.delete_notification, name="delete_notification"),
    # path('notifications', login_required(NotificationsView.as_view(), login_url='/login'), name="notifications"),

    path('quiz/<slug:slug>/data', views.quiz_data_view, name='quiz-data'),

    path('explore', views.explore, name="explore"),
    path('explore/<str:category>', views.categories, name="category"),
    path('search', views.search, name="search"),
    path('follow/<str:username>/', views.follow, name="follow"),
    path('unfollow/<str:username>/', views.unfollow, name="unfollow"),
    path('settings', login_required(SettingsView.as_view(), login_url="/login"), name="settings"),
    path('settings/theme', login_required(views.personalize, login_url="/login"), name="theme"),
    path('update/avatar', views.update_avatar, name="update_avatar"),
    path('auth/login', views.login_view, name="login"),
    path('auth/register', Register.as_view(), name="register"),
    path('delete/account', views.delete_account, name="delete_account"),
    path('logout', views.logout_view, name="logout"),
]
