# Django Libs
from django.contrib.auth.models import User

# Django REST Libs
from rest_framework.test import (APITestCase,)


class UserTests(APITestCase):
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
