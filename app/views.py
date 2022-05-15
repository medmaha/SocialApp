from itertools import chain
from turtle import Vec2D
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from app.forms import ProfileFrom, ProfileImageForm

from posts.models import Comment, Video
from posts.forms import VideoForm
from users.models import Profile


def register_user(request):
    if request.POST.get('email'):
        email = request.POST['email']
        username = request.POST['username']
        fullname = request.POST['fullname']
        password = request.POST['password']

        User.objects.create_user(
            email=email, username=username, first_name=fullname, password=password)

        return redirect('login')
    return render(request, 'register.html')


def login_user(request):
    user = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            ''

        if user:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')

    return render(request, 'login.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):

    if not request.user.is_authenticated:
        return redirect('login')

    videos = Video.objects.all()

    my_feed = []
    for video in videos:
        if request.user in video.likes.all():
            my_feed.append(video.id)

    my_videos = Video.objects.filter(author=request.user)
    for my_video in my_videos:
        my_feed.append(my_video.id)

    my_feed = Video.objects.filter(id__in=my_feed).order_by('-date_posted')

    return render(request, 'index.html', {
        'videos': my_feed
    })


@login_required(login_url='login')
def create_post(request):
    form = VideoForm()
    if request.method == 'POST':
        title = request.POST['title']
        print(request.POST)

        form = VideoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.slug = title.strip()

            new_post.save()
            return redirect('index')
    return render(request, 'add-post.html', {
        'form': form
    })


@login_required(login_url='login')
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    video_posts = Video.objects.filter(author=user)

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'videos': video_posts
    })


@login_required(login_url='login')
def edit_profile(request, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)

    profile_form = ProfileFrom(instance=user)
    image_form = ProfileImageForm(instance=profile)

    if request.method == 'POST':
        profile_form = ProfileFrom(instance=user, data=request.POST)
        image_form = ProfileImageForm(instance=profile, files=request.FILES)

        if profile_form.is_valid() and image_form.is_valid():
            profile_form.save()
            image_form.save()
            return HttpResponseRedirect(reverse('profile', kwargs={'user_id':  user.id}))
        messages.error(request, 'Bad request with the form')

    return render(request, 'edit-profile.html', {
        'image_form': image_form,
        'profile_form': profile_form,
    })


@login_required(login_url='login')
def follow_unfollow(request, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)

    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def like_dislike_post(request, video_id):
    video = Video.objects.get(id=video_id)
    liked_by_users = video.likes.all()

    is_like = False
    for user in liked_by_users:
        if user == request.user:
            is_like = True

    if is_like:
        video.likes.remove(request.user)

    if not is_like:
        video.likes.add(request.user)

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def make_comment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment').strip()
        post_id = request.POST.get('post_id')

        try:
            video = Video.objects.get(id=post_id)
        except:
            messages.success(request, 'Bad request')
            return redirect(request.META['HTTP_REFERER'])

        if comment:
            Comment.objects.create(
                author=request.user,
                body=comment,
                post=video
            )
        print(comment, post_id)
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def explore_posts(request):
    videos = Video.objects.all().order_by('-date_posted')

    return render(request, 'explore.html', {
        'videos': videos
    })
