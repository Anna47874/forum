from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.forum_home,name="forum_home"),
    path("register/", views.register_view,name="register"),
    path("login/", views.UserLoginView.as_view(),name="login"),
    path("logout/", views.UserLogoutView.as_view(),name="logout"),
    path("posts/new/", views.create_post,name="create_post"),
    path("posts/<int:post_id>/edit/", views.edit_post,name="edit_post"),
    path("posts/<int:post_id>/delete/", views.delete_post,name="delete_post"),
    path("posts/<int:post_id>/comment/", views.create_comment,name="post_comments"),
]