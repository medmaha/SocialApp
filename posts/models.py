from django.db import models
# from users.models import AppUser
from django.contrib.auth.models import User


def videos_path(instance, filename):
    name = instance.title.replace(' ', '-')
    return f'posts/{name[:12]}/{filename}'


class Video(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author', null=True)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=videos_path)
    slug = models.SlugField(blank=True)
    likes = models.ManyToManyField(
        User, related_name='likes')

    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:50]
