# -*- coding: utf-8 -*-
import shortuuid
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# generate random short url
def short_url_generator():
    return f"{shortuuid.uuid()[0:8]}"


# function for getting title in <h1> tag
def get_title(url):
    try:
        html = urlopen(url)
    except HTTPError:
        print("This web-page: " + url + " is not defined.")
        return None
    try:
        soup = BeautifulSoup(html.read(), "html.parser")
        title = soup.find('h1').getText()
    except AttributeError:
        print("Tag was not found")
        return None
    return title


def paginate(obj, current_page, pages):
    paginator = Paginator(obj, pages)
    try:
        result = paginator.page(current_page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result


def save_user_urls(user, url):
    user_urls = list(user.profile.urls.all())
    user_urls.append(url)
    user.profile.urls.set(user_urls)
    user.save()
