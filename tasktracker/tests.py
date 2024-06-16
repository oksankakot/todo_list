from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Task
from user.models import User

class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', first_name='Test')
        self.superuser = User.objects.create_superuser(username='admin', password='password', first_name='Admin')
        self.client = APIClient()
        self.client.login(username='testuser', password='password')
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='new',
            user=self.user
        )

    def obtain_token(self, username, password):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': username, 'password': password}, format='json')
        return response.data['access']

    def test_create_task(self):
        token = self.obtain_token('testuser', 'password')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('task-create')
        data = {
            "title": "New Task",
            "description": "Task description",
            "status": "new"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.get(id=2).title, 'New Task')

    def test_get_all_tasks(self):
        token = self.obtain_token('testuser', 'password')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('all-tasks-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Поскольку у вас используется пагинация

    def test_get_user_tasks(self):
        token = self.obtain_token('testuser', 'password')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('user-tasks-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Поскольку у вас используется пагинация

    def test_get_task_detail(self):
        token = self.obtain_token('testuser', 'password')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_update_task(self):
        token = self.obtain_token('testuser', 'password')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('task-update', kwargs={'pk': self.task.id})
        data = {
            "title": "Updated Task"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_delete_task(self):
        token = self.obtain_token('testuser', 'password')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('task-delete', kwargs={'pk': self.task.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
