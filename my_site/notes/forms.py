from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150,label="Nickname")
    class Meta:
        model = User
        fields = ["username","password1","password2"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text","image"]
        widgets = {
            "text":forms.Textarea(attrs={"rows":3})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text":forms.Textarea(attrs={"rows":3})
        }