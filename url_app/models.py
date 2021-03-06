import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from url_manager.settings import DEFAULT_DOMAIN


class Profile(models.Model):
    """To keep extra user data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "Users Profiles"

    name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name="User Name")

    email_confirmed = models.BooleanField(default=False)

    urls = models.ManyToManyField('Url',
                                  verbose_name="Urls",
                                  blank=True,)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        p = Profile.objects.create(user=instance, name=instance.username)
        p.save()
    instance.profile.save()


class Url(models.Model):
    """Url Model"""

    class Meta:
        """docstring for Meta"""
        verbose_name = "Url"
        verbose_name_plural = "Urls"

    uuid = models.UUIDField(
        verbose_name="UUID",
        default=uuid.uuid4,
        editable=False,
        unique=True)

    url = models.URLField(
        unique=False,
        verbose_name="URL",
        blank=False)

    title = models.CharField(
        max_length=256,
        blank=True,
        verbose_name="Text")

    domain = models.CharField(
        max_length=96,
        blank=True,
        verbose_name="Domain",
        default=DEFAULT_DOMAIN)

    short_url = models.CharField(
        max_length=256,
        blank=True,
        unique=True,
        verbose_name="Short URL")

    slug = models.SlugField(
        unique=False,
        verbose_name="Slug",
        default=short_url)

    clicks = models.IntegerField(
        blank=True,
        verbose_name="Clicks",
        default=0)

    create_dttm = models.DateTimeField(
        verbose_name="Created",
        blank=True,
        default=datetime.now)

    def __str__(self):
        return f"URL: {self.url}. Short url: {self.short_url}"
