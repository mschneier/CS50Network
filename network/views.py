from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json


@login_required
def index(request):
    posts = Post.objects.order_by("date")
    return render(request, "network/index.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def newPost(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user.id
        likes = 0
        post = Post.objects.create(content, user, likes)
        messages.success(request, "Post created.")
        return redirect("/profile")
    return render(request, "network/newPost.html")
        

@login_required
def editPost(request, postID):
    post = Post.objects.get(id=postID)
    content = post.content
    userID = post.user
    if request.user.id != userID:
        messages.error(
            request, "You do not have permission to edit this post."
        )
        return redirect("/allposts")
    if request.method == "POST":
        content = request.POST["content"]
        post.update(content=content)
        messages.success(request, "You updated this post.")
        return redirect("/profile")
    return render(request, "network/editPost.html", {
        "content": content
    })


@login_required
def profile(request, userID):
    user = User.objects.get(id=userID)
    posts = Post.objects.filter(user=userID)
    following = user.following
    followed_by = user.followed_by
    return render(request, "network/profile.html", {
        "posts": posts, "following": following, "followed_by": followed_by
    })


@login_required
def followedPosts(request):
    following = User.objects.filter(id=request.user.id).following
    posts = {}
    followedUsers = [
        User.objects.get(id=userID).username for userID in following
    ]
    for user in followedUsers:
        userID = User.objects.filter(username=user).id
        posts[user] = Post.objects.filter(id=userID)
    return render(request, "network/following.html", {
        "posts": posts
    })


@csrf_exempt
@login_required
def changeLikeStatus(request, postID):
    try:
        post = Post.objects.get(id=postID)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "PUT":
        data = json.loads(request.body)
        if request.user.id in post.liked_by:
            post.liked_by.remove(request.user.id)
            post.likes -= 1
        else:
            post.liked_by.add(request.user.id)
            post.likes += 1
        post.save()
        return HttpResponse(status=204)
    return JsonResponse({
        "error": "PUT request required."
    }, status=400)
