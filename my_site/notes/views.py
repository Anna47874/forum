from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden


from .models import Post,Comment
from .forms import RegisterForm, PostForm, CommentForm

def forum_home(request):
    posts = Post.objects.select_related("nickname").prefetch_related("comments__nickname").order_by("-post_date")
    return render(request,"forum_home.html",{"posts":posts})

def register_view(request):
    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user =form.save()
            login(request,user)
            return redirect("forum_home")
    else:
        form = RegisterForm()
    return render(request,"register.html",{"form":form})

class UserLoginView(LoginView):
    template_name = "login.html"
    next_page=reverse_lazy("forum_home")

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
    return render(request,"post_form.html",{"form":form,"title":"Створення поста"})


@login_required
def edit_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if post.nickname!=request.user:
        return redirect("forum_home")
    if request.method=="POST":
        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post =form.save(commit=False)
            if "image" not in request.FILES:
                if post.image:
                    post.image.delete(save = False)
                post.image=None
            form.save()
            return redirect("forum_home")
    else:
        form = PostForm(instance=post)
    return render(request,"post_form.html",{"form":form,"title":"Змінення посту","post":post})


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
    return render(request,"post_delete.html",{"form":form,"post":post})

def post_comments(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    comments = Comment.objects.filter(post_id=post_id).select_related("nickname").order_by("-post_date")
    return render(request,"post_comments.html",{"post":post,"comments":comments})

@login_required
def create_comment(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if request.method=="POST":
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            c =form.save(commit=False)
            c.post = post
            c.nickname=request.user
            c.save()
            return redirect("post_comments",post_id=post.id)
    else:
        form = CommentForm()
    return render(request,"create_comment.html",{"form":form,"post":post,})

@login_required
def edit_comment(request,comment_id,post_id):
    comment=get_object_or_404(Comment,id=comment_id)
    post=get_object_or_404(Post,id=post_id)
    if comment.nickname!=request.user:
        return redirect("post_comments",post_id=post.id)
    if request.method=="POST":
        form = CommentForm(request.POST,request.FILES,instance=comment)
        if form.is_valid():
            comment =form.save(commit=False)
            if "image" not in request.FILES:
                if comment.image:
                    comment.image.delete(save = False)
                comment.image=None
            form.save()
            return redirect("post_comments",post_id=post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request,"edit_comment.html",{"form":form,"title":"Змінення коментарю","comment":comment})

@login_required
def delete_comment(request,comment_id,post_id):
    comment=get_object_or_404(Comment,id=comment_id)
    if comment.nickname!=request.user:
        return redirect("post_comments",post_id=post_id)
    if request.method=="POST":
        comment.delete()
        return redirect("post_comments",post_id=post_id)
    return render(request,"delete_comment.html",{"title":"Видалення коментарю","comment":comment,"post_id":post_id})
