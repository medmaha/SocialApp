from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image
import uuid


def profile_path(instance, filename):
    return f'profiles/{instance.user.username[:15]}/{filename}'


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name='id',
                          unique=True, editable=False, default=uuid.uuid4,)
    avater = models.ImageField(
        upload_to=profile_path, default='profiles/default.png', null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    followers = models.ManyToManyField(
        User, related_name='followers', blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=Profile)
def crop_profile_img(sender, instance, created, **kwargs):
    if instance.avater:
        if not created or not created:
            img = Image.open(instance.avater.path)
            thumbnails = (200, 200)
            img.thumbnail(thumbnails)
            img.save(instance.avater.path)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
