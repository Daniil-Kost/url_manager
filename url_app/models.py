# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from url_manager.settings import DEFAULT_DOMAIN


# Create your models here.
class Url(models.Model):
    """Url Model"""

    class Meta:
        """docstring for Meta"""
        verbose_name = "Url"
        verbose_name_plural = "Urls"

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
        max_length=8,
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
