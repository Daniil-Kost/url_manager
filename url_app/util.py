import shortuuid
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from url_manager.settings import DEFAULT_DOMAIN


# generate random short url
def short_url_generator():
    return f"{shortuuid.uuid()[0:8]}"


# function for getting title in <h1> tag
def get_title(url):
    try:
        html = urlopen(url)
    except HTTPError:
        print("This web-page: " + url + " is not defined.")
        return ""
    try:
        soup = BeautifulSoup(html.read(), "html.parser")
        title = soup.find('h1').getText()
    except AttributeError:
        print("Tag was not found")
        return ""
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


def prepare_url_data(data):
    val = URLValidator()
    errors = {}
    try:
        val(data["url"])
        title = get_title(data["url"])
        data["title"] = title
    except ValidationError:
        data['url'] = u"Your long URL is invalid"
        data["title"] = ""

    if data.get("short_url"):
        if 4 > len(data["short_url"]) or len(data["short_url"]) > 8:
            errors['short_url'] = "Short URL will be at least" \
                                  " 4 chars and max 8 chars"
    if not data.get("short_url") or data.get("short_url") == "":
        data["short_url"] = f'{DEFAULT_DOMAIN}{short_url_generator()}'

    return data, errors
