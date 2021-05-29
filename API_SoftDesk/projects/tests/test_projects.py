# Django Libs
from django.contrib.auth.models import User

# Django REST Libs
from rest_framework.test import (APITestCase,)


class ProjectTests(APITestCase):
    """
    Tests for project management.

    Tests :
        Authenticated user tests : (AUT)
            Generics tests: (GT)
                + create project (cp)
            Author tests: (AT)
                + list projects (lp)
                + retrieve project (rp)
                + update project (up)
                + delete project (dp)
            Contributors tests: (CT)
                + list projects (lp)
                + retrieve projects (rp)
                - update project (up)
                - delete project (dp)
            No contributors test: (NCT)
                + list projects (lp)
                - retrieve project (rp)
                - update project (up)
                - delete project (dp)
        Unauthenticated user tests : (UUT)
            - list projects (lp)
            - create project (cp)
            - retrieve project (rp)
            - update project (up)
            - delete project (dp)
    """

    def setUp(self):
        """Setup
            - first user
            - contributor user
            - no contributor user
        """
        # first user
        user_form = {
            'username': 'user1',
            'last_name': 'TEST',
            'first_name': 'user',
            'password': 'Motdepasse123',
            'email': 'test@test.com',
        }
        user = User.objects.create_user(**user_form)
        user.save()
        # contributor user
        user_form = {
            'username': 'user2',
            'last_name': 'TEST',
            'first_name': 'user',
            'password': 'Motdepasse123',
            'email': 'test@test.com',
        }
        user = User.objects.create_user(**user_form)
        user.save()
        # no contributor user
        user_form = {
            'username': 'user3',
            'last_name': 'TEST',
            'first_name': 'user',
            'password': 'Motdepasse123',
            'email': 'test@test.com',
        }
        user = User.objects.create_user(**user_form)
        user.save()

    def test_AUT_GT_cp(self):
        """Test
        Authenticated user /
            Generic Test /
                + create project
        attempt : 201
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        response = self.client.post(url, project, format='json')
        self.assertEqual(response.status_code, 201)

    def test_AUT_AT_lp_none(self):
        """Test
        Authenticated user /
            Author Test /
                + list projects
        attempt : 204
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        self.client.force_authenticate(user=user)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 204)

    def test_AUT_AT_lp(self):
        """Test
        Authenticated user /
            Author Test /
                + list projects
        attempt : 200
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_AT_rp(self):
        """Test
        Authenticated user /
            Author Test /
                + retrieve project
        Attempt : 200
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')
        url = 'http://127.0.0.1:8000/projects/1/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_AT_up(self):
        """Test
        Authenticated user /
            Author Test /
                + update project
        Attempt : 200
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')

        url = 'http://127.0.0.1:8000/projects/1/'
        project_form = {
            'title': 'test',
        }
        response = self.client.put(path=url, data=project_form)
        self.assertEqual(response.status_code, 200)

    def test_AUT_AT_dp(self):
        """Test
        Authenticated user /
            Author Test /
                + delete project
        Attempt : 200
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')

        url = 'http://127.0.0.1:8000/projects/1/'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_CT_lp(self):
        """Test
        Authenticated user /
            Contributor Test /
                + list projects
        attempt : 200
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')

        url = 'http://127.0.0.1:8000/projects/1/users/'
        contrib_form = {'user_id': '2'}
        self.client.post(path=url,
                         data=contrib_form)
        user2 = User.objects.get(username='user2')
        self.client.force_authenticate(user=user2)
        url = 'http://127.0.0.1:8000/projects/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_CT_rp(self):
        """Test
        Authenticated user /
            Contributor Test /
                + retrieve project
        attempt : 200
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')

        url = 'http://127.0.0.1:8000/projects/1/users/'
        contrib_form = {'user_id': '2'}
        self.client.post(path=url,
                         data=contrib_form)
        user2 = User.objects.get(username='user2')
        self.client.force_authenticate(user=user2)
        url = 'http://127.0.0.1:8000/projects/1/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_CT_up(self):
        """Test
        Authenticated user /
            Contributor Test /
                - update project
        attempt : 403
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')

        url = 'http://127.0.0.1:8000/projects/1/users/'
        contrib_form = {'user_id': '2'}
        self.client.post(path=url,
                         data=contrib_form)
        user2 = User.objects.get(username='user2')
        self.client.force_authenticate(user=user2)
        url = 'http://127.0.0.1:8000/projects/1/'
        project_form = {
            'title': 'test'
        }
        response = self.client.post(path=url, data=project_form)
        self.assertEqual(response.status_code, 403)

    def test_AUT_CT_dp(self):
        """Test
        Authenticated user /
            Contributor Test /
                - delete project
        attempt : 403
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')

        url = 'http://127.0.0.1:8000/projects/1/users/'
        contrib_form = {'user_id': '2'}
        self.client.post(path=url,
                         data=contrib_form)
        user2 = User.objects.get(username='user2')
        self.client.force_authenticate(user=user2)
        url = 'http://127.0.0.1:8000/projects/1/'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_lp(self):
        """Test
        Authenticated user /
            No contributor Test /
                + list project
        Attempt : 204
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')

        user3 = User.objects.get(username='user3')
        self.client.force_authenticate(user=user3)
        url = 'http://127.0.0.1:8000/projects/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 204)

    def test_AUT_NCT_rp(self):
        """Test
        Authenticated user /
            No contributor Test /
                - retrieve project
        attempt : 403
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')

        user3 = User.objects.get(username='user3')
        self.client.force_authenticate(user=user3)
        url = 'http://127.0.0.1:8000/projects/1/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_up(self):
        """Test
        Authenticated user /
            No contributor Test /
                - update project
        attempt : 403
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')

        user3 = User.objects.get(username='user3')
        self.client.force_authenticate(user=user3)
        url = 'http://127.0.0.1:8000/projects/1/'
        project_form = {
            'title': 'test',
        }
        response = self.client.put(path=url, data=project_form)
        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_dp(self):
        """Test
        Authenticated user /
            No contributor Test /
                - delete project
        attempt : 403
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')

        user3 = User.objects.get(username='user3')
        self.client.force_authenticate(user=user3)
        url = 'http://127.0.0.1:8000/projects/1/'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 403)

    def test_UUT_lp(self):
        """Test
        Unauthenticated user /
            - list projects
        attempt : 401
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')
        self.client.logout()

        url = 'http://127.0.0.1:8000/projects/'
        response = self.client.put(path=url)
        self.assertEqual(response.status_code, 401)

    def test_UUT_cp(self):
        """Test
        Unauthenticated user /
            - create project
        attempt : 401
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')
        self.client.logout()

        url = 'http://127.0.0.1:8000/projects/'
        project_form = {
            'title': 'test',
            'description': 'project test',
            'type': 'test'
        }
        response = self.client.post(path=url, data=project_form)
        self.assertEqual(response.status_code, 401)

    def test_UUT_rp(self):
        """Test
        Unauthenticated user /
            - retrieve project
        attempt : 401
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')
        self.client.logout()

        url = 'http://127.0.0.1:8000/projects/1/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 401)

    def test_UUT_up(self):
        """Test
        Unauthenticated user /
            - update project
        attempt : 401
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')
        self.client.logout()

        url = 'http://127.0.0.1:8000/projects/1/'
        project_form = {
            'title': 'test',
        }
        response = self.client.put(path=url, data=project_form)
        self.assertEqual(response.status_code, 401)

    def test_UUT_dp(self):
        """Test
        Unauthenticated user /
            - delete project
        attempt : 401
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/'
        project = {'title': 'project',
                   'description': 'project test',
                   'type': 'test'}
        self.client.force_authenticate(user=user)
        self.client.post(url, project, format='json')
        self.client.logout()

        url = 'http://127.0.0.1:8000/projects/1/'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 401)
