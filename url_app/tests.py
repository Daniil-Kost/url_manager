from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from url_manager.urls import api_version
from url_app.models import Url
from .test_fixtures.mock_for_tests import URLS, post_success_data
from url_app import util


# Create your tests here.
class ApiResourcesTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        for url in URLS:
            record = Url.objects.create(url=url[0], short_url=url[1], title=" ")
            record.save()
        password = "TestPass!2222"
        user = User.objects.create_user(username="test_user", password=password)
        user.save()
        self.urls = Url.objects.all()
        for url in self.urls:
            util.save_user_urls(user, url)
        data = {"username": user.username, "password": password}
        response = self.client.post(f"/api-token-auth/", data, format='json')
        token = response.data["token"]
        self.headers = {"Content-Type": "application/json", "Authorization": f"Token {token}"}
        self.client.login(username=user.username, password=password)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def test_get_all_urls_for_user_success(self):
        response = self.client.get(f"/{api_version}urls", headers=self.headers)
        data = list(response.data)
        self.assertEqual(3, len(data))
        self.assertEqual(200, response.status_code)
        self.assertIn("short_url", data[0])

    def test_get_all_urls_for_user_failed_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token dnsjfdfjbfjdsbdfbjdbf')
        response = self.client.get(f"/{api_version}urls", headers=self.headers)
        self.assertEqual(401, response.status_code)

    def test_post_new_url_success(self):
        response = self.client.post(f"/{api_version}urls", post_success_data, format='json')
        uuid = response.data["uuid"]
        get_response = self.client.get(f"/{api_version}urls", headers=self.headers)
        user_uuids_list = [resp['uuid'] for resp in get_response.data]
        self.assertEqual(201, response.status_code)
        self.assertIn("short_url", response.data)
        self.assertIn("uuid", response.data)
        self.assertIn("title", response.data)
        self.assertIn(uuid, user_uuids_list)

    def test_post_new_url_success(self):
        response = self.client.post(f"/{api_version}urls", post_success_data, format='json')
        uuid = response.data["uuid"]
        get_response = self.client.get(f"/{api_version}urls", headers=self.headers)
        user_uuids_list = [resp['uuid'] for resp in get_response.data]
        self.assertEqual(201, response.status_code)
        self.assertIn("short_url", response.data)
        self.assertIn("uuid", response.data)
        self.assertIn("title", response.data)
        self.assertIn(uuid, user_uuids_list)

    def test_post_new_url_failed_with_invalid_data(self):
        response = self.client.post(f"/{api_version}urls", {}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid data. Please define 'url' in your request data.")

