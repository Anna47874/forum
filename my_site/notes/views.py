from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden

from .models import Post
from .forms import RegisterForm, PostForm, CommentForm

def forum_home(request):
    posts = Post.objects.select_related("nickname").prefetch_related("comments__nickname").order_by("-created_at")
    return render(request,"templates/forum_home.html",{"posts":posts})

def register_view(request):
    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user =form.save()
            login(request,user)
            return redirect("forum_home")
    else:
        form = RegisterForm()
    return render(request,"templates/register.html",{"form":form})

class UserLoginView(LoginView):
    template_name = "templates/login.html"

class UserLogoutView(LogoutView):
    next_page=reverse_lazy("forum_home")

@login_required
def create_post(request):
    if request.method=="POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post =form.save(commit=False)
            post.nickname=request.user
            post.save()
            return redirect("forum_home")
    else:
        form = PostForm()
    return render(request,"templates/post_form.html",{"form":form,"title":"create_post"})


@login_required
def edit_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if post.nickname!=request.user:
        return redirect("forum_home")
    if request.method=="POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("forum_home")
    else:
        form = PostForm(instance=post)
    return render(request,"templates/post_form.html",{"form":form,"title":"edit_post"})


@login_required
def delete_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if post.nickname!=request.user:
        return redirect("forum_home")
    if request.method=="POST":
        post.delete()
        return redirect("forum_home")
    else:
        form = PostForm(instance=post)
    return render(request,"templates/post_delete.html",{"form":form})



def create_comment(request,post_id):
    post=get_object_or_404(Post.objects.select_related("nickname").prefetch_related("comments__nickname"),id=post_id)
    comments=post.comments.all().order_by("created_at")
    if request.method=="POST":
        if not request.user.is_authenticated:
            return redirect("login")
        form = CommentForm(request.POST)
        if form.is_valid():
            c =form.save(commit=False)
            c.post = post
            c.nickname=request.user
            c.save()
            return redirect("post_comments")
    else:
        form = CommentForm()
    return render(request,"templates/post_comments.html",{"form":form,"post":post,"comments":comments})