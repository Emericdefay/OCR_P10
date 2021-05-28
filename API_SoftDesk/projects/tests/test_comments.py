# Django Libs
from django.contrib.auth.models import User

# Django REST Libs
from rest_framework.test import (APITestCase,)

# Locals Libs
from ..models import (Project,
                      Contributor,
                      Issue,)


class CommentTests(APITestCase):
    """
    Tests for comments management.

    Tests :
        Authenticated user tests : (AUT)
            Author tests: (AT)
                + list comments (lc)
                + add comment (ac)
                + retrieve comments (rc)
                + update comments (uc)
                + delete comments (dc)
            Contributors tests: (CT)
                + list comments (lc)
                + add comment (ac)
                + retrieve comments (rc)
                - update comments (uc)
                - delete comments (dc)
            No contributors test: (NCT)
                - list comments (lc)
                - add comment (ac)
                - retrieve comments (rc)
                - update comments (uc)
                - delete comments (dc)

        Unauthenticated user tests : (UUT)
            - list comments (lc)
            - add comment (ac)
            - retrieve comments (rc)
            - update comments (uc)
            - delete comments (dc)
    """

    def setUp(self):
        """Setup
        Users
            - author user
            - contributor user
            - no contributor user
        Projet
            - example project
        Issue
            - example issue for project
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

        # Set author main contributor
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

        # example issue
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
            'assignee_user_id': contrib_user,
            'author_user_id': author_user,
            'project_id': project
        }
        issue = Issue(**issue_form)
        issue.save()

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

    def test_AUT_AT_lc_nc(self):
        """Test
        Authenticate user /
            Author user /
                + list comments
                no content (nc)
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 204)

    def test_AUT_AT_lc_c(self):
        """Test
        Authenticate user /
            Author user /
                + list comments
                with content (c)
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_AT_ac(self):
        """Test
        Authenticate user /
            Author user /
                + add comment
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        response = self.client.post(path=url, data=comment_form)
        self.assertEqual(response.status_code, 201)

    def test_AUT_AT_rc(self):
        """Test
        Authenticate user /
            Author user /
                + retrieve comment
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/1/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_AT_uc(self):
        """Test
        Authenticate user /
            Author user /
                + update comment
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/1/'
        updated_form = {
            'description': 'modified comment'
        }
        response = self.client.put(path=url, data=updated_form)
        self.assertEqual(response.status_code, 200)

    def test_AUT_AT_dc(self):
        """Test
        Authenticate user /
            Author user /
                + delete comment
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/1/'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_CT_lc(self):
        """Test
        Authenticate user /
            Contributor user /
                + list comments
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)

        user2 = User.objects.get(username='user2')
        self.client.force_authenticate(user=user2)
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, 200)

    def test_AUT_CT_ac(self):
        """Test
        Authenticate user /
            Contributor user /
                + add comment
        """
        user2 = User.objects.get(username='user2')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user2)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_AUT_CT_rc(self):
        """Test
        Authenticate user /
            Contributor user /
                + retrieve comment
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/1/'
        user2 = User.objects.get(username='user2')
        self.client.force_authenticate(user=user2)
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, 200)

    def test_AUT_CT_uc(self):
        """Test
        Authenticate user /
            Contributor user /
                - update comment
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/1/'
        user2 = User.objects.get(username='user2')
        self.client.force_authenticate(user=user2)
        updated_form = {
            'description': 'unauthorize update'
        }

        response = self.client.put(path=url, data=updated_form)

        self.assertEqual(response.status_code, 403)

    def test_AUT_CT_dc(self):
        """Test
        Authenticate user /
            Contributor user /
                - delete comment
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/1/'
        user2 = User.objects.get(username='user2')
        self.client.force_authenticate(user=user2)

        response = self.client.delete(path=url)

        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_lc(self):
        """Test
        Authenticate user /
            No contributor user /
                - list comments
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        user3 = User.objects.get(username='user3')
        self.client.force_authenticate(user=user3)

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_ac(self):
        """Test
        Authenticate user /
            No contributor user /
                - add comment
        """
        user3 = User.objects.get(username='user3')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user3)
        comment_form = {
            'description': 'test comment',
        }
        response = self.client.post(path=url, data=comment_form)

        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_rc(self):
        """Test
        Authenticate user /
            No contributor user /
                - retrieve comment
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/1/'
        user3 = User.objects.get(username='user3')
        self.client.force_authenticate(user=user3)

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_uc(self):
        """Test
        Authenticate user /
            No contributor user /
                - update comment
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/1/'
        user3 = User.objects.get(username='user3')
        self.client.force_authenticate(user=user3)
        updated_form = {
            'description': 'unauthorized update'
        }
        response = self.client.put(path=url, data=updated_form)

        self.assertEqual(response.status_code, 403)

    def test_AUT_NCT_dc(self):
        """Test
        Authenticate user /
            No contributor user /
                - delete comment
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)

        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/1/'
        user3 = User.objects.get(username='user3')
        self.client.force_authenticate(user=user3)
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 403)

    def test_UUT_lc(self):
        """Test
        Unauthenticate user /
            - list comments
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)
        self.client.logout()

        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 401)

    def test_UUT_ac(self):
        """Test
        Unauthenticate user /
            - add comment
        """
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        comment_form = {
            'description': 'test comment',
        }
        response = self.client.post(path=url, data=comment_form)
        self.assertEqual(response.status_code, 401)

    def test_UUT_rc(self):
        """Test
        Unauthenticate user /
            - retrieve comment
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)
        self.client.logout()

        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/1/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 401)

    def test_UUT_uc(self):
        """Test
        Unauthenticate user /
            - update comment
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)
        self.client.logout()

        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        updated_comment = {
            'description': 'unauthorized comment'
        }
        response = self.client.put(path=url, data=updated_comment)
        self.assertEqual(response.status_code, 401)

    def test_UUT_dc(self):
        """Test
        Unauthenticate user /
            - delete comment
        """
        user = User.objects.get(username='user1')
        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/'
        self.client.force_authenticate(user=user)
        comment_form = {
            'description': 'test comment',
        }
        self.client.post(path=url, data=comment_form)
        self.client.logout()

        url = 'http://127.0.0.1:8000/projects/1/issues/1/comments/1/'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, 401)
