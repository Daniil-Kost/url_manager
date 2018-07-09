# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime


# Create your models here.
class MyUrl(models.Model):
    """MyUrl Model"""

    class Meta(object):
        """docstring for Meta"""
        verbose_name = "MyUrl"
        verbose_name_plural = "MyUrls"

    url = models.URLField(
        unique=False,
        verbose_name="URL",
        blank=False)

    text = models.TextField(
        blank=True,
        verbose_name="Text")

    domain = models.CharField(
        max_length=128,
        blank=True,
        verbose_name="Domain",
        default="http://localhost:8000/")

    short_url = models.CharField(
        max_length=6,
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
        return "URL: %s. Short url: %s" % (
            self.url, self.short_url)
