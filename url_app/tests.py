from django.test import TestCase
from unittest.mock import Mock, patch
import requests
from django.contrib.auth.models import User
import pprint

from url_manager.settings import DEFAULT_DOMAIN
from url_manager.urls import api_version
from url_app.models import Url, Profile
from .test_fixtures.mock_for_tests import URLS
from url_app import util


# Create your tests here.
class ApiResourcesTests(TestCase):

    def setUp(self):
        # create urls objects
        for url in URLS:
            u = Url.objects.create(url=url[0], short_url=url[1], title=" ")
            u.save()
        password = "TestPass!2222"
        user = User.objects.create_user(username="test", password=password)
        user.save()
        urls = Url.objects.all()
        pprint.pprint("#" * 50)
        pprint.pprint(list(urls))
        for url in urls:
            util.save_user_urls(user, url)
        data = {"username": user.username, "password": password}
        response = self.client.post(f"{DEFAULT_DOMAIN}api-token-auth/", data=data)
        token = response.json()["token"]
        self.headers = {"Content-Type": "application/json", "Authorization": f"Token {token}"}
        self.client.login(**data)
        pprint.pprint(")" * 50)
        pprint.pprint(user.is_authenticated)

    def test_get_all_urls_for_user_success(self):
        response = requests.get(f"{DEFAULT_DOMAIN}{api_version}urls", headers=self.headers)
        pprint.pprint("!" * 50)
        pprint.pprint(self.headers)
        data = response.json()
        pprint.pprint("+" * 50)
        pprint.pprint(data)
        self.assertEqual(3, len(data))
        self.assertEqual(200, response.status_code)
        self.assertIn("short_url", data[0])
