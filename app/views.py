from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from posts.models import Video
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

#    New Feature
    liked_videos = []
    videos = Video.objects.all()

    for video in videos:
        if request.user in video.likes.all():
            liked_videos.append(video)

    return render(request, 'index.html', {
        'videos': liked_videos
    })


@login_required(login_url='login')
def create_post(request):
    form = VideoForm()
    if request.method == 'POST':
        title = request.POST['title']

        form = VideoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.slug = title
            form.author = request.user
            form.save()
            return redirect('index')
        print(request.POST)
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
        'profile':profile,
        'videos': video_posts
    })


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
def explore_posts(request):
    videos = Video.objects.all().order_by('-date_posted')

    return render(request, 'explore.html', {
        'videos': videos
    })
