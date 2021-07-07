from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Follow

import json

def index(request):
    return render(request, "network/index.html", {
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

@csrf_exempt
@login_required 
def create_post(request):
    
    #only allow through post
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    #create post object from request
    data = json.loads(request.body)
    content = data.get("content", "")
    post = Post(content=content, poster=request.user)
    post.save()

    return JsonResponse({"message": "Post createed successfully"}, status=201)

@login_required
def get_post(request, username):
    #Filter
    if username == "all":
        posts = Post.objects.all()
    elif username == "following":
        following = [follow.following for follow in request.user.followings.all()]
        if len(following) > 0:
            posts = following[0].posts.all()
            for each in following:
                posts =  posts.union(each.posts.all())
        else: 
            posts = None
                
    else:
        user = User.objects.get(username=username)
        posts = user.posts.all()
        
        #if posts.first() is  None:
        #    return JsonResponse({"error": "Can't find post by the requested user."}, status=400)
    if posts != None:
        posts = posts.order_by("-timestamp").all()

        #whether or not active_user has liked the post
        serialized_posts = []
        user_like = request.user.user_like.all()
        for post in posts:
            temp = post.serialize()
            temp['liked'] = any(post.id == each.post.id for each in user_like)
            serialized_posts.append(temp)

        return JsonResponse(serialized_posts, safe=False)
    else:
        return JsonResponse([], safe=False)

@login_required
def get_user(request, username):
    user = User.objects.get(username=username)

    #whether active_user is following visiting_user
    is_following = any(username == follow.following.username for follow in request.user.followings.all())
    return JsonResponse([user.serialize(), {'is_following':is_following}], safe=False)

@csrf_exempt
@login_required
def follow(request):

    if request.method != "POST":
        return JsonResponse({"error":"POST request required."},  status=400)
    
    #create Follow object
    data = json.loads(request.body)

    following = data.get("following", "")
    following_user = User.objects.get(username=following)
    follow = Follow(follower=request.user, following=following_user)
    follow.save()

    request.user.num_following += 1
    following_user.num_follower += 1
    request.user.save()
    following_user.save()

    return JsonResponse({"message": "Follow request is successful."}, status=201)

@csrf_exempt
@login_required
def like(request, post_id):

    if  request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    
    post = Post.objects.get(id=post_id)
    post.like += 1
    post.save()

    like = Like(liker=request.user, post=post)
    like.save()


    return JsonResponse({"message": "Like request is successful."}, status=201) 

@csrf_exempt
@login_required
def unlike(request, post_id):

    if  request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    
    post = Post.objects.get(id=post_id)
    post.like -= 1
    post.save()

    Like.objects.get(liker=request.user, post=post).delete()

    return JsonResponse({"message": "Unlike request is successful."}, status=201)
