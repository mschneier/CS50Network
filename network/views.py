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
    posts = [
        {"content": post.content,
        "id": post.id,
        "date": post.date,
        "likes": post.likes,
        "liked_by": post.liked_by.all(),
        "userID": post.user.id,
        "user": post.user.username,
        } for post in posts
    ]
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
        user = User.objects.get(id=request.user.id)
        likes = 0
        post = Post.objects.create(
            content=content, user=user, likes=likes
        )
        messages.success(request, "Post created.")
        return redirect(f"/profile/{request.user.id}")
    return render(request, "network/newPost.html")
        

@login_required
def editPost(request, postID):
    post = Post.objects.get(id=postID)
    content = post.content
    userID = post.user.id
    if request.user.id != userID:
        messages.error(
            request, "You do not have permission to edit this post."
        )
        return redirect("/")
    if request.method == "POST":
        content = request.POST.get("content", "")
        Post.objects.filter(id=postID).update(content=content)
        messages.success(request, "You updated this post.")
        return redirect(f"/profile/{request.user.id}")
    return render(request, "network/editPost.html", {
        "content": content, "postID": post.id
    })


@login_required
def profile(request, userID):
    user = User.objects.get(id=userID)
    posts = Post.objects.filter(user=userID).order_by("-date")
    followingCount = user.following.count()
    followedByCount = user.followed_by.count()
    following = user.following.all()
    profilePosts = [
        {"content": post.content,
        "id": post.id,
        "date": post.date,
        "likes": post.likes,
        "liked_by": post.liked_by.all(),
        "userID": post.user.id,
        } for post in posts
    ]
    return render(request, "network/profile.html", {
        "posts": profilePosts, "followingCount": followingCount,
        "username": user.username, "followedByCount": followedByCount,
        "following": following, "userID": int(userID),
    })


@login_required
def followedPosts(request):
    following = User.objects.get(id=request.user.id).following.all()
    posts = {}
    followedUsers = [
        User.objects.get(id=userID).username for userID in following
    ]
    for user in followedUsers:
        userID = User.objects.filter(username=user).id
        posts[user] = Post.objects.filter(id=userID)
    if posts:
        for post in posts:
            post = [
                {"content": p.content,
                "id": p.id,
                "date": p.date,
                "likes": p.likes,
                "liked_by": p.liked_by.all(),
                "userID": p.user.id,
                } for p in post
            ]
        return render(request, "network/following.html", {
            "posts": posts, "following": following,
        })
    return render(request, "network/nofollowing.html")


@csrf_exempt
@login_required
def changeLikeStatus(request, postID):
    try:
        post = Post.objects.get(id=postID)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "PUT":
        if post.likes == 0:
            post.liked_by.add(request.user)
            post.likes += 1
        else:
            likeUsers = list(post.liked_by.all())
            if request.user in likeUsers:
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


@csrf_exempt
@login_required
def changeFollowStatus(request, userID):
    try:
        currentUser = User.objects.get(id=request.user.id)
        followedUser = User.objects.get(id=userID)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
    if request.method == "PUT":
        if userID == request.user.id:
            return JsonResponse({
                "error": "You can't follow yourself."
            }, status=403)
        if userID in list(currentUser.following.all()):
            currentUser.following.remove(userID)
            followedUser.followed_by.remove(request.user.id)
        else:
            currentUser.following.add(userID)
            followedUser.followed_by.add(request.user.id)
        currentUser.save()
        followedUser.save()
        return HttpResponse(status=204)
    return JsonResponse({
        "error": "PUT request required."
    }, status=400)
