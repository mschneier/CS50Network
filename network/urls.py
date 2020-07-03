
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newPost, name="newpost"),
    path("editpost/<postID>", views.editPost, name="editpost"),
    path("profile/<userID>", views.profile, name="profile"),
    path("followedposts", views.followedPosts, name="followedposts")
]
