
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #api
    path("posts", views.create_post, name="new_post"),
    path("posts/like/<int:post_id>", views.like, name="like"),
    path("posts/unlike/<int:post_id>", views.unlike, name="unlike"),
    path("posts/<str:username>", views.get_post, name="get_post"),
    #user_related
    path("users/follow", views.follow, name="follow"),
    path("users/<str:username>", views.get_user, name="get_user")
    
]
