# Django Libs
from django.contrib.auth.models import User

# Django REST Libs
from rest_framework.test import (APITestCase,)

# Locals Libs
from ..models import (Project,
                      Contributor,
                      Issue,
                      Comment)


class IssueTests(APITestCase):
    """
    Tests for issues management.

    Tests :
        Authenticated user tests : (AUT)
            Author tests: (AT)
                + list issues (li)
                + add issue (ai)
                - retrieve issues (ri)
                + update issues (ui)
                + delete issues (di)
            Contributors tests: (CT)
                + list issues (li)
                + add issue (ai)
                - retrieve issues (ri)
                - update issues (ui)
                - delete issues (di)
            No contributors test: (NCT)
                - list issues (li)
                - add issue (ai)
                - retrieve issues (ri)
                - update issues (ui)
                - delete issues (di)

        Unauthenticated user tests : (UUT)
            - list issues (li)
            - add issue (ai)
            - retrieve issues (ri)
            - update issues (ui)
            - delete issues (di)
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

        author_contrib = {
            'user_id': author_user,
            'project_id': project,
            'role': 'author',
            'permission': '1'
        }

        author = Contributor(**author_contrib)
        author.save()

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

    def test_AUT_AT_li(self):
        """Test
        Authenticate user /
            Author user /
                + list issues
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        self.client.force_authenticate(user=user)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_AT_ai_a(self):
        """Test
        Authenticate user /
            Author user /
                + add issue
                with assignee_user_id
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        self.client.force_authenticate(user=user)
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
            'assignee_user_id': 2,
        }
        response = self.client.post(path=url, data=issue_form)
        self.assertEqual(response.status_code, 201)

    def test_AUT_AT_ai_na(self):
        """Test
        Authenticate user /
            Author user /
                + add issue
                without assignee_user_id
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        self.client.force_authenticate(user=user)
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        response = self.client.post(path=url, data=issue_form)
        self.assertEqual(response.status_code, 201)
        
    def test_AUT_AT_ri(self):
        """Test
        Authenticate user /
            Author user /
                - retrieve issue
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        self.client.force_authenticate(user=user)
        self.client.post(path=url, data=issue_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 403)

    def test_AUT_AT_ui(self):
        """Test
        Authenticate user /
            Author user /
                + update issue
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        self.client.force_authenticate(user=user)
        self.client.post(path=url, data=issue_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/'

        updated_form = {
            'title': 'test issue'
        }

        response = self.client.put(path=url, data=updated_form)

        self.assertEqual(response.status_code, 200)

    def test_AUT_AT_di(self):
        """Test
        Authenticate user /
            Author user /
                + delete issue
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        self.client.force_authenticate(user=user)
        self.client.post(path=url, data=issue_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_CT_li(self):
        """Test
        Authenticate user /
            Contributor user /
                + list issues
        """
        user = User.objects.get(username='user2')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        self.client.force_authenticate(user=user)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_CT_ai(self):
        """Test
        Authenticate user /
            Contributor user /
                + add issue
        """
        user = User.objects.get(username='user2')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        self.client.force_authenticate(user=user)
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
            'assignee_user_id': 1,
        }
        response = self.client.post(path=url, data=issue_form)
        self.assertEqual(response.status_code, 201)

    def test_AUT_CT_ri(self):
        """Test
        Authenticate user /
            Contributor user /
                - retrieve issue
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        self.client.force_authenticate(user=user)
        self.client.post(path=url, data=issue_form)
        user2 = User.objects.get(username='user2')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/'
        self.client.force_authenticate(user=user2)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 403)

    def test_AUT_CT_ui(self):
        """Test
        Authenticate user /
            Contributor user /
                - update issue
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        self.client.force_authenticate(user=user)
        self.client.post(path=url, data=issue_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/'
        user2 = User.objects.get(username='user2')
        self.client.force_authenticate(user=user2)

        updated_form = {
            'title': 'test issue'
        }

        response = self.client.put(path=url, data=updated_form)

        self.assertEqual(response.status_code, 403)

    def test_AUT_CT_di(self):
        """Test
        Authenticate user /
            Contributor user /
                - delete issue
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        self.client.force_authenticate(user=user)
        self.client.post(path=url, data=issue_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/'
        user2 = User.objects.get(username='user2')
        self.client.force_authenticate(user=user2)
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_li(self):
        """Test
        Authenticate user /
            No contributor user /
                - list issues
        """
        user = User.objects.get(username='user3')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        self.client.force_authenticate(user=user)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_ai(self):
        """Test
        Authenticate user /
            No contributor user /
                - add issue
        """
        user = User.objects.get(username='user3')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        self.client.force_authenticate(user=user)
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        response = self.client.post(path=url, data=issue_form)
        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_ri(self):
        """Test
        Authenticate user /
            No contributor user /
                - retrieve issue
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        self.client.force_authenticate(user=user)
        self.client.post(path=url, data=issue_form)
        user3 = User.objects.get(username='user3')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/'
        self.client.force_authenticate(user=user3)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_ui(self):
        """Test
        Authenticate user /
            No contributor user /
                - update issue
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        self.client.force_authenticate(user=user)
        self.client.post(path=url, data=issue_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/'
        user3 = User.objects.get(username='user3')
        self.client.force_authenticate(user=user3)
        updated_form = {
            'title': 'test issue'
        }
        response = self.client.put(path=url, data=updated_form)
        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_di(self):
        """Test
        Authenticate user /
            No contributor user /
                - delete issue
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        self.client.force_authenticate(user=user)
        self.client.post(path=url, data=issue_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/'
        user3 = User.objects.get(username='user3')
        self.client.force_authenticate(user=user3)
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 403)

    def test_UUT_li(self):
        """Test
        Unauthenticate user /
            - list issues
        """
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 401)

    def test_UUT_ai(self):
        """Test
        Unauthenticate user /
            - add issue
        """
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        response = self.client.post(path=url, data=issue_form)
        self.assertEqual(response.status_code, 401)

    def test_UUT_ri(self):
        """Test
        Unauthenticate user /
            - retrieve issue
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        self.client.force_authenticate(user=user)
        self.client.post(path=url, data=issue_form)
        self.client.logout()

        url = 'http://127.0.0.1:8000/projects/1/issues/1/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 401)

    def test_UUT_ui(self):
        """Test
        Unauthenticate user /
            - update issue
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        self.client.force_authenticate(user=user)
        self.client.post(path=url, data=issue_form)
        self.client.logout()

        url = 'http://127.0.0.1:8000/projects/1/issues/1/'
        updated_form = {
            'title': 'issue test'
        }
        response = self.client.put(path=url, data= updated_form)
        self.assertEqual(response.status_code, 401)

    def test_UUT_di(self):
        """Test
        Unauthenticate user /
            - delete issue
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/'
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
        }
        self.client.force_authenticate(user=user)
        self.client.post(path=url, data=issue_form)
        self.client.logout()
        
        url = 'http://127.0.0.1:8000/projects/1/issues/1/'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 401)