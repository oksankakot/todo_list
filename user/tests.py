from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password", first_name="Test"
        )
        self.superuser = User.objects.create_superuser(
            username="admin", password="password", first_name="Admin"
        )
        self.client = APIClient()

    def obtain_token(self, username, password):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"username": username, "password": password}, format="json"
        )
        return response.data["access"]

    def test_create_user(self):
        url = reverse("user-list-create")
        data = {
            "username": "newuser",
            "password": "newpassword",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_get_user(self):
        token = self.obtain_token("testuser", "password")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        url = reverse("user-detail", kwargs={"pk": self.user.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_update_user(self):
        token = self.obtain_token("testuser", "password")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        url = reverse("user-detail", kwargs={"pk": self.user.id})
        data = {
            "username": "testuser",
            "password": "password",
            "first_name": "Updated",
            "last_name": self.user.last_name,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

    def test_delete_user(self):
        token = self.obtain_token("testuser", "password")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        url = reverse("user-detail", kwargs={"pk": self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)
