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
    path("posts/<int:post_id>/post-comments/", views.post_comments,name="post_comments"),
    path("posts/<int:post_id>/new-comment/", views.create_comment,name="create_comment"),
    path("posts/<int:comment_id>/edit-comment/<int:post_id>/", views.edit_comment,name="edit_comment"),
    path("posts/<int:comment_id>/delete-comment/<int:post_id>/", views.delete_comment,name="delete_comment"),
]