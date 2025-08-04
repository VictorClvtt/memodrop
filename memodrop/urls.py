from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.Register.as_view(), name="register"),
    path("login/", views.Login.as_view(), name="login"),
    path("", views.Main.as_view(), name="main"),
    path("friendships/", views.Friendship.as_view(), name="friendships"),

    path("user/<int:id>/memos", views.Memos.as_view(), name="memos"),
]