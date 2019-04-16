from url_manager.settings import DEFAULT_DOMAIN
from url_app import util

URLS = [
    ("http://devacademy.ru/posts/ochered-soobschenij-i-asinhronnyie-zadachi-s-pomoschyu-celery-i-rabbitmq/",
     f"{DEFAULT_DOMAIN}{util.short_url_generator()}"),
    ("https://docs.djangoproject.com/en/2.1/ref/models/querysets/",
     f"{DEFAULT_DOMAIN}{util.short_url_generator()}"),
    ("https://stackoverflow.com/questions/9943504/right-to-left-string-replace-in-python",
     f"{DEFAULT_DOMAIN}{util.short_url_generator()}")
]


post_success_data = {"url": "https://www.django-rest-framework.org/tutorial/3-class-based-views/"}
