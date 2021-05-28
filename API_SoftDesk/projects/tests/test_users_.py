# Django Libs
from django.contrib.auth.models import User

# Django REST Libs
from rest_framework.test import (APITestCase,)


class SigninTests(APITestCase):
    """
    """
    def test_signup(self):
        """Test
        attempt : 201
        """
        user_form = {
            'username': 'user1',
            'last_name': 'TEST',
            'first_name': 'user',
            'password': 'Motdepasse123',
            'email': 'test@test.com',
        }
        url = 'http://127.0.0.1:8000/signup/'
        response = self.client.post(url, user_form, format='json')
        self.assertEqual(response.status_code, 201)


class LoginTest(APITestCase):
    """
    """

    def setUp(self):

        user_form = {
            'username': 'user1',
            'last_name': 'TEST',
            'first_name': 'user',
            'password': 'Motdepasse123',
            'email': 'test@test.com',
        }
        user = User.objects.create_user(**user_form)
        user.save()

    def test_login(self):
        """Test
            login
        """
        url = 'http://127.0.0.1:8000/login/'
        user_form = {
            'username': 'user1',
            'password': 'Motdepasse123'
        }
        response = self.client.post(path=url, data=user_form)
        self.assertEqual(response.status_code, 200)
