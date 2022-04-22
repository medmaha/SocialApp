from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('create-post/', views.create_post, name='create-post'),
    path('profile/<int:user_id>', views.user_profile, name='profile'),

    path('like-dislike/<int:video_id>',
         views.like_dislike_post, name='like-dislike'),
]
