from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", views.Register.as_view(), name="register"),
    path("login/", views.Login.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path("", views.Home.as_view(), name="home"),
    path("friendships/", views.Friendship.as_view(), name="friendships"),

    path("user/<int:id>/memos", views.Memos.as_view(), name="memos"),
]