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
                + retrieve issues (ri)
                + update issues (ui)
                + delete issues (di)
            Contributors tests: (CT)
                + list issues (li)
                + add issue (ai)
                + retrieve issues (ri)
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

        # example issue
        issue_form = {
            'title': 'issue',
            'desc': 'issue desc',
            'tag': 'test',
            'priority': 'low',
            'status': 'created',
            'assignee_user_id': 2,
        }

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
    def test_AUT_AT_ai(self):
        """Test
        Authenticate user /
            Author user /
                + add issue
        """
    def test_AUT_AT_ri(self):
        """Test
        Authenticate user /
            Author user /
                + retrieve issue
        """
    def test_AUT_AT_ui(self):
        """Test
        Authenticate user /
            Author user /
                + update issue
        """
    def test_AUT_AT_di(self):
        """Test
        Authenticate user /
            Author user /
                + delete issue
        """

    def test_AUT_CT_li(self):
        """Test
        Authenticate user /
            Contributor user /
                + list issues
        """
    def test_AUT_CT_ai(self):
        """Test
        Authenticate user /
            Contributor user /
                + add issue
        """
    def test_AUT_CT_ri(self):
        """Test
        Authenticate user /
            Contributor user /
                + retrieve issue
        """
    def test_AUT_CT_ui(self):
        """Test
        Authenticate user /
            Contributor user /
                - update issue
        """
    def test_AUT_CT_di(self):
        """Test
        Authenticate user /
            Contributor user /
                - delete issue
        """

    def test_AUT_NCT_li(self):
        """Test
        Authenticate user /
            No contributor user /
                - issues
        """
    def test_AUT_NCT_ai(self):
        """Test
        Authenticate user /
            No contributor user /
                - add issue
        """
    def test_AUT_NCT_ri(self):
        """Test
        Authenticate user /
            No contributor user /
                - retrieve issue
        """
    def test_AUT_NCT_ui(self):
        """Test
        Authenticate user /
            No contributor user /
                - update issue
        """
    def test_AUT_NCT_di(self):
        """Test
        Authenticate user /
            No contributor user /
                - delete issue
        """

    def test_UUT_li(self):
        """Test
        Unauthenticate user /
            - list issues
        """
    def test_UUT_ai(self):
        """Test
        Unauthenticate user /
            - add issue
        """
    def test_UUT_ri(self):
        """Test
        Unauthenticate user /
            - retrieve issue
        """
    def test_UUT_ui(self):
        """Test
        Unauthenticate user /
            - update issue
        """
    def test_UUT_di(self):
        """Test
        Unauthenticate user /
            - delete issue
        """