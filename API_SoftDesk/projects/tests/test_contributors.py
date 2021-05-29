# Django Libs
from django.contrib.auth.models import User

# Django REST Libs
from rest_framework.test import (APITestCase,)

# Locals Libs
from ..models import (Project,
                      Contributor,)


class ContributorTests(APITestCase):
    """
    Tests for contributor management.

    Tests :
        Authenticated user tests : (AUT)
            Author tests: (AT)
                + list contributors (lc)
                + add contributor (ac)
                + delete contributors (dc)
                - retrieve contributors (rc)
                - update contributors (uc)
            Contributors tests: (CT)
                + list contributors (lc)
                - add contributor (ac)
                - retrieve contributors (rc)
                - update contributors (uc)
                - delete contributors (dc)
            No contributors test: (NCT)
                - add contributor (ac)
                - list contributors (lc)
                - retrieve contributors (rc)
                - update contributors (uc)
                - delete contributors (dc)

        Unauthenticated user tests : (UUT)
            - add contributor (ac)
            - list contributors (lc)
            - retrieve contributors (rc)
            - update contributors (uc)
            - delete contributors (dc)
    """

    def setUp(self):
        """Setup
        Users
            - author user
            - contributor user
            - no contributor user
        Projet
            - example project
        """
        # author user
        user_form = {
            'username': 'user1',
            'last_name': 'TEST',
            'first_name': 'user',
            'password': 'Motdepasse123',
            'email': 'test@test.com',
        }
        author_user = User.objects.create_user(**user_form)
        author_user.save()

        # example project
        project_form = {
            'title': 'project',
            'description': 'project test',
            'type': 'test',
            'author_user_id': author_user,
        }
        project = Project(**project_form)
        project.save()

        # contributor user
        user_form = {
            'username': 'user2',
            'last_name': 'TEST',
            'first_name': 'user',
            'password': 'Motdepasse123',
            'email': 'test@test.com',
        }
        contrib_user = User.objects.create_user(**user_form)
        contrib_user.save()

        contrib_form = {
            'user_id': contrib_user,
            'project_id': project,
            'role': 'test',
            'permission': '0',
        }
        contrib = Contributor(**contrib_form)
        contrib.save()

        # no contributor user
        user_form = {
            'username': 'user3',
            'last_name': 'TEST',
            'first_name': 'user',
            'password': 'Motdepasse123',
            'email': 'test@test.com',
        }
        no_contrib_user = User.objects.create_user(**user_form)
        no_contrib_user.save()

    def test_AUT_AT_lc(self):
        """Test
        Authenticated user /
            Author user /
                + list contributors
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/users/'
        self.client.force_authenticate(user=user)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_AT_ac_exist(self):
        """Test
        Authenticated user /
            Author user /
                + add contributor
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/users/'
        self.client.force_authenticate(user=user)
        contrib_form = {
            "user_id": '2',
        }
        response = self.client.post(path=url, data=contrib_form)
        self.assertEqual(response.status_code, 208)

    def test_AUT_AT_ac(self):
        """Test
        Authenticated user /
            Author user /
                + add contributor
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/users/'
        self.client.force_authenticate(user=user)
        contrib_form = {
            "user_id": '3',
        }
        response = self.client.post(path=url, data=contrib_form)
        self.assertEqual(response.status_code, 201)

    def test_AUT_AT_dc(self):
        """Test
        Authenticated user /
            Author user /
                + delete contributor
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/users/'
        self.client.force_authenticate(user=user)
        contrib_form = {
            "user_id": '3',
        }
        self.client.post(path=url, data=contrib_form)

        url = 'http://127.0.0.1:8000/projects/1/users/3/'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_AT_rc(self):
        """Test
        Authenticated user /
            Author user /
                - retrieve contributor
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/users/1/'
        self.client.force_authenticate(user=user)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 403)

    def test_AUT_AT_uc(self):
        """Test
        Authenticated user /
            Author user /
                - update contributor
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/users/1/'
        self.client.force_authenticate(user=user)
        contrib_form = {
            'user_id': '2'
        }
        response = self.client.put(path=url, data=contrib_form)
        self.assertEqual(response.status_code, 403)

    def test_AUT_CT_lc(self):
        """Test
        Authenticated user /
            Contributor user /
                + list contributor
        """
        user = User.objects.get(username='user2')
        url = 'http://127.0.0.1:8000/projects/1/users/'
        self.client.force_authenticate(user=user)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_CT_ac(self):
        """Test
        Authenticated user /
            Contributor user /
                - add contributor
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        self.client.force_authenticate(user=user)
        project_2 = {
            'title': 'project',
            'description': 'project test',
            'type': 'test',
        }
        self.client.post(path=url, data=project_2)

        user2 = User.objects.get(username='user2')
        url = 'http://127.0.0.1:8000/projects/2/users/'
        self.client.force_authenticate(user=user2)
        contrib_form = {
            "user_id": '3',
        }
        response = self.client.post(path=url, data=contrib_form)
        self.assertEqual(response.status_code, 403)

    def test_AUT_CT_rc(self):
        """Test
        Authenticated user /
            Contributor user /
                - retrieve contributor
        """
        user = User.objects.get(username='user2')
        url = 'http://127.0.0.1:8000/projects/1/users/1/'
        self.client.force_authenticate(user=user)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 403)

    def test_AUT_CT_uc(self):
        """Test
        Authenticated user /
            Contributor user /
                - update contributor
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        self.client.force_authenticate(user=user)
        project_2 = {
            'title': 'project',
            'description': 'project test',
            'type': 'test',
        }
        self.client.post(path=url, data=project_2)

        user2 = User.objects.get(username='user2')
        url = 'http://127.0.0.1:8000/projects/2/users/'
        self.client.force_authenticate(user=user2)
        contrib_form = {
            "user_id": '3',
        }
        response = self.client.put(path=url, data=contrib_form)
        self.assertEqual(response.status_code, 403)

    def test_AUT_CT_dc(self):
        """Test
        Authenticated user /
            Contributor user /
                - delete contributor
        """
        user2 = User.objects.get(username='user2')
        url = 'http://127.0.0.1:8000/projects/2/users/'
        self.client.force_authenticate(user=user2)
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_ac(self):
        """Test
        Authenticated user /
            No contributor user /
                - add contributor
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        self.client.force_authenticate(user=user)
        project_2 = {
            'title': 'project',
            'description': 'project test',
            'type': 'test',
        }
        self.client.post(path=url, data=project_2)

        user3 = User.objects.get(username='user3')
        url = 'http://127.0.0.1:8000/projects/2/users/'
        self.client.force_authenticate(user=user3)
        contrib_form = {
            "user_id": '3',
        }
        response = self.client.post(path=url, data=contrib_form)
        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_lc(self):
        """Test
        Authenticated user /
            No contributor user /
                - list contributor
        """
        user3 = User.objects.get(username='user3')
        url = 'http://127.0.0.1:8000/projects/2/users/'
        self.client.force_authenticate(user=user3)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 404)

    def test_AUT_NCT_rc(self):
        """Test
        Authenticated user /
            No contributor user /
                - retrieve contributor
        """
        user3 = User.objects.get(username='user3')
        url = 'http://127.0.0.1:8000/projects/2/users/1/'
        self.client.force_authenticate(user=user3)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_uc(self):
        """Test
        Authenticated user /
            No contributor user /
                - update contributor
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        self.client.force_authenticate(user=user)
        project_2 = {
            'title': 'project',
            'description': 'project test',
            'type': 'test',
        }
        self.client.post(path=url, data=project_2)

        user3 = User.objects.get(username='user3')
        url = 'http://127.0.0.1:8000/projects/2/users/'
        self.client.force_authenticate(user=user3)
        contrib_form = {
            "user_id": '3',
        }
        response = self.client.put(path=url, data=contrib_form)
        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_dc(self):
        """Test
        Authenticated user /
            No contributor user /
                - delete contributor
        """
        user3 = User.objects.get(username='user3')
        url = 'http://127.0.0.1:8000/projects/1/users/2/'
        self.client.force_authenticate(user=user3)
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 403)

    def test_UUT_ac(self):
        """Test
        Unauthenticated user /
            - add contributor
        """
        url = 'http://127.0.0.1:8000/projects/1/users/'

        contrib_form = {
            "user_id": "3"
        }

        response = self.client.post(path=url, data=contrib_form)
        self.assertEqual(response.status_code, 401)

    def test_UUT_lc(self):
        """Test
        Unauthenticated user /
            - list contributor
        """
        url = 'http://127.0.0.1:8000/projects/1/users/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 401)

    def test_UUT_rc(self):
        """Test
        Unauthenticated user /
            - retrieve contributor
        """
        url = 'http://127.0.0.1:8000/projects/1/users/1/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 401)

    def test_UUT_uc(self):
        """Test
        Unauthenticated user /
            - update contributor
        """
        url = 'http://127.0.0.1:8000/projects/1/users/1/'

        contrib_form = {
            'user_id': '3'
        }

        response = self.client.put(path=url, data=contrib_form)
        self.assertEqual(response.status_code, 401)

    def test_UUT_dc(self):
        """Test
        Unauthenticated user /
            - delete contributor
        """
        url = 'http://127.0.0.1:8000/projects/1/users/1/'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 401)
