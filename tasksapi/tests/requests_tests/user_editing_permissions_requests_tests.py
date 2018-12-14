"""Contains tests for user editing permissions."""

from rest_framework import status
from rest_framework.test import APITestCase
from tasksapi.models import User

# Put data about our fixtures as constants here


class UserEditPermissionsRequestsTests(APITestCase):
    """Test user editing permissions."""

    fixtures = ["test-fixture.yaml"]

    def test_test(self):
        # TODO finish me up
        pass
