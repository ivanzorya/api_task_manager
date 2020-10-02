import uuid
from datetime import datetime, timedelta
from random import randrange

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from .models import Task

DATE_1 = datetime.strptime('10/10/2020', '%m/%d/%Y')
DATE_2 = datetime.strptime('10/10/2021', '%m/%d/%Y')
DATE_3 = datetime.strptime('11/10/2021', '%m/%d/%Y')
DATE_4 = datetime.strptime('10/10/2022', '%m/%d/%Y')


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


class TaskManagerTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = uuid.uuid4().hex
        self.password = uuid.uuid4().hex
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.username_not_author = uuid.uuid4().hex
        self.password_not_author = uuid.uuid4().hex
        self.user_no_author = User.objects.create_user(
            username=self.username_not_author,
            password=self.password_not_author
        )
        self.new_username = uuid.uuid4().hex
        self.new_password = uuid.uuid4().hex
        self.title = uuid.uuid4().hex
        self.new_title = uuid.uuid4().hex
        self.description = uuid.uuid4().hex
        self.new_description = uuid.uuid4().hex
        self.completed = str(random_date(DATE_1, DATE_2).date())
        self.new_completed = str(random_date(DATE_3, DATE_4).date())
        self.status = ['new', 'planned', 'work', 'completed']
        self.task = Task.objects.create(
            title=self.title,
            author=self.user,
            completed=self.completed
        )
        response_token_author = self.client.post(
            '/api/v1/token/',
            {'username': self.username, 'password': self.password}
        )
        self.token_author = response_token_author.json().get('access')
        response_token_not_author = self.client.post(
            '/api/v1/token/',
            {
                'username': self.username_not_author,
                'password': self.password_not_author
            }
        )
        self.token_not_author = response_token_not_author.json().get('access')

    def test_get_token(self):
        response_token = self.client.post('/api/v1/token/')
        self.assertEqual(response_token.status_code, 400)
        response_token = self.client.post(
            '/api/v1/token/',
            {'username': self.username, 'password': self.password}
        )
        response = response_token.json()
        self.assertEqual(response_token.status_code, 200)
        self.assertIn('access', response)
        self.assertIn('refresh', response)

    def test_get_task(self):
        response_tasks = self.client.get(
            '/api/v1/tasks/',
            HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        self.assertEqual(response_tasks.status_code, 200)
        response = response_tasks.json()
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertEqual(self.title, response[0].get('title'))
        self.assertIn(self.status[0], response[0].get('status'))
        response_task = self.client.get(
            '/api/v1/tasks/1/',
            HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        self.assertEqual(response_task.status_code, 200)
        response = response_task.json()
        self.assertIsInstance(response, dict)
        self.assertEqual(self.username, response.get('author'))
        response_task_not_author = self.client.get(
            '/api/v1/tasks/1/',
            HTTP_AUTHORIZATION=f'Bearer {self.token_not_author}')
        self.assertEqual(response_task_not_author.status_code, 404)

    def test_create_task(self):
        response_create = self.client.post(
            '/api/v1/tasks/',
            {
                'title': self.title,
                'description': self.description,
                'completed': self.completed
            },
            HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        self.assertEqual(response_create.status_code, 201)
        new_task = Task.objects.get(pk=2)
        self.assertEqual(str(new_task.completed), self.completed)
        self.assertEqual(new_task.author, self.user)
        response_tasks = self.client.get(
            '/api/v1/tasks/',
            HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        response = response_tasks.json()
        self.assertEqual(len(response), 2)

    def test_delete_task(self):
        response_delete = self.client.delete(
            '/api/v1/tasks/1/',
            HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        self.assertEqual(response_delete.status_code, 204)
        response_delete = self.client.get(
            '/api/v1/tasks/1/',
            HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        self.assertEqual(response_delete.status_code, 404)

    def test_change(self):
        response_change = self.client.patch(
            '/api/v1/tasks/1/',
            {'description': self.new_description,
             'status': self.status[1]
             },
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        self.assertEqual(response_change.status_code, 200)
        response_change = self.client.get(
            '/api/v1/tasks/1/changes/',
            HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        self.assertEqual(response_change.status_code, 200)
        response = response_change.json()
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 2)
        response_change = self.client.get(
            '/api/v1/tasks/1/changes/1/',
            HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        self.assertEqual(response_change.status_code, 200)
        response = response_change.json()
        self.assertIsInstance(response, dict)
        self.assertEqual('', response.get('old_value'))
        self.assertEqual(self.new_description, response.get('new_value'))
        response_change = self.client.get(
            '/api/v1/tasks/1/changes/2/',
            HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        self.assertEqual(response_change.status_code, 200)
        response = response_change.json()
        self.assertIsInstance(response, dict)
        self.assertEqual(self.status[0], response.get('old_value'))
        self.assertEqual(self.status[1], response.get('new_value'))
        response_change = self.client.patch(
            '/api/v1/tasks/1/',
            {'completed': self.new_completed,
             'status': self.status[2]
             },
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        response_change = self.client.get(
            '/api/v1/tasks/1/changes/',
            HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        self.assertEqual(response_change.status_code, 200)
        response = response_change.json()
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 4)

    def test_auth(self):
        response_auth = self.client.post('/api/v1/auth/')
        self.assertEqual(response_auth.status_code, 400)
        self.assertContains(
            response_auth,
            'This field is required.',
            count=2,
            status_code=400,
            html=False
        )
        response_auth = self.client.post(
            '/api/v1/auth/',
            {
                'username': self.new_username,
                'password': self.new_password
            }
        )
        self.assertEqual(response_auth.status_code, 201)
        response_token = self.client.post(
            '/api/v1/token/',
            {'username': self.new_username, 'password': self.new_password}
        )
        token = response_token.json().get('access')
        self.assertEqual(response_token.status_code, 200)
        response_get = self.client.get(
            '/api/v1/tasks/',
            HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response_get.status_code, 200)
        response = response_get.json()
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 0)
        response_change = self.client.get(
            '/api/v1/tasks/1/',
            HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response_change.status_code, 404)
