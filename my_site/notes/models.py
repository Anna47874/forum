from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    nickname =models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    text = models.TextField()
    image = models.ImageField(upload_to="images/",blank=True,null=True)
    post_date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post =models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    nickname =models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    text = models.TextField()
    image = models.ImageField(upload_to="images/",blank=True,null=True)
    post_date = models.DateTimeField(auto_now_add=True)