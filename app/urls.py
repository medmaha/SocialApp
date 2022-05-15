from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('create-post/', views.create_post, name='create-post'),
    path('explore-posts/', views.explore_posts, name='explore'),

    path('profile/<int:user_id>/', views.user_profile, name='profile'),
    path('edit/profile/<int:user_id>/', views.edit_profile, name='edit-profile'),
    path('follow/profile/<int:user_id>/',
         views.follow_unfollow, name='follow'),

    path('like-dislike/<int:video_id>/',
         views.like_dislike_post, name='like-dislike'),
    path('comment/',
         views.make_comment, name='comment'),
]
