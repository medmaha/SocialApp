from email.policy import default
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


def profile_path(instance, filename):
    return f'profiles/{instance.username[:15]}/{filename}'


class CustumAccountManager(BaseUserManager):
    def create_super_user(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_active') is not True:
            raise ValueError(_(
                'Superuser must be assign is_active=True'
            ))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_(
                'Superuser must be assign is_superuser=True'
            ))
        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):
        email = self.normalize_email
        user = self.model(email=email, username=username,
                          password=password, **other_fields)
        if not email:
            raise ValueError(_('You must provide an email address'))

        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email_address'), unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(_('bio'), max_length=500, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    profile = models.ImageField(
        upload_to=profile_path, default='profiles/default.png', null=True)
    date_stated = models.DateTimeField(auto_now_add=True)

    objects = CustumAccountManager
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
