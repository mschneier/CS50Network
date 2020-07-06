
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("newpost/", views.newPost, name="newpost"),
    path("editpost/<postID>/", views.editPost, name="editpost"),
    path("profile/<userID>/", views.profile, name="profile"),
    path("followedposts/", views.followedPosts, name="followedposts"),
    path(
        "changelikestatus/<postID>/", views.changeLikeStatus,
        name="changelikestatus"
    ),
    path(
        "changefollowstatus/<userID>/", views.changeFollowStatus,
        name="changefollowstatus"
    ),
]
