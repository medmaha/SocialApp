from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image
import uuid


def profile_path(instance, filename):
    return f'profiles/{instance.username[:15]}/{filename}'


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

    def save(self, *args, **kwargs):
        img = Image.open(self.avater.path)
        thumbnails = (70, 70)
        img.thumbnail(thumbnails)
        img.save(self.avater.path)
        return super().save(args, kwargs)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
