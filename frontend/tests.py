"""Contains tests for the front-end."""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

ADMIN_USER_USERNAME = "adminuser"
ADMIN_USER_PASSWORD = "qwertyuiop"
EXECUTABLE_TASK_INSTANCE_UUID = "aa07248f-fdf3-4d34-8215-0c7b21b892ad"
CONTAINER_TASK_INSTANCE_UUID = "e7133970-ac3c-4026-adcf-55ee170d4eb3"
EXECUTABLE_TASK_TYPE_PK = 1
CONTAINER_TASK_TYPE_PK = 1
TASK_QUEUE_PK = 1


class FrontendRenderTests(TestCase):
    """Just make sure pages render properly."""

    fixtures = ["test-fixture.yaml"]

    def setUp(self):
        """Authenticate the client in."""
        login_response = self.client.post(
            reverse("login"),
            {"username": ADMIN_USER_USERNAME, "password": ADMIN_USER_PASSWORD},
        )

        self.assertEqual(login_response.status_code, status.HTTP_302_FOUND)

    def test_getting_frontend_pages(self):
        """Try GETting a bunch of pages."""
        # Build a list of pages to iterate over that return the same
        # status code. The ordering here isn't significant, but its in
        # the order that the URLs appear in the urls module.
        pages_to_get = [
            reverse("home"),
            reverse("about"),
            reverse("account-edit-profile"),
            reverse("account-change-password"),
            reverse("containertaskinstance-list"),
            reverse("containertaskinstance-create-menu"),
            reverse(
                "containertaskinstance-detail",
                kwargs={"uuid": CONTAINER_TASK_INSTANCE_UUID},
            ),
            reverse(
                "containertaskinstance-rename",
                kwargs={"uuid": CONTAINER_TASK_INSTANCE_UUID},
            ),
            reverse(
                "containertaskinstance-clone",
                kwargs={"uuid": CONTAINER_TASK_INSTANCE_UUID},
            ),
            reverse(
                "containertaskinstance-stateupdate",
                kwargs={"uuid": CONTAINER_TASK_INSTANCE_UUID},
            ),
            reverse(
                "containertaskinstance-terminate",
                kwargs={"uuid": CONTAINER_TASK_INSTANCE_UUID},
            ),
            reverse(
                "containertaskinstance-delete",
                kwargs={"uuid": CONTAINER_TASK_INSTANCE_UUID},
            ),
            reverse("containertasktype-list"),
            reverse("containertasktype-create"),
            reverse(
                "containertasktype-detail",
                kwargs={"pk": CONTAINER_TASK_TYPE_PK},
            ),
            reverse(
                "containertaskinstance-create",
                kwargs={"pk": CONTAINER_TASK_TYPE_PK},
            ),
            reverse(
                "containertasktype-delete",
                kwargs={"pk": CONTAINER_TASK_TYPE_PK},
            ),
            reverse(
                "containertasktype-update",
                kwargs={"pk": CONTAINER_TASK_TYPE_PK},
            ),
            reverse("executabletaskinstance-list"),
            reverse("executabletaskinstance-create-menu"),
            reverse(
                "executabletaskinstance-detail",
                kwargs={"uuid": EXECUTABLE_TASK_INSTANCE_UUID},
            ),
            reverse(
                "executabletaskinstance-rename",
                kwargs={"uuid": EXECUTABLE_TASK_INSTANCE_UUID},
            ),
            reverse(
                "executabletaskinstance-clone",
                kwargs={"uuid": EXECUTABLE_TASK_INSTANCE_UUID},
            ),
            reverse(
                "executabletaskinstance-stateupdate",
                kwargs={"uuid": EXECUTABLE_TASK_INSTANCE_UUID},
            ),
            reverse(
                "executabletaskinstance-terminate",
                kwargs={"uuid": EXECUTABLE_TASK_INSTANCE_UUID},
            ),
            reverse(
                "executabletaskinstance-delete",
                kwargs={"uuid": EXECUTABLE_TASK_INSTANCE_UUID},
            ),
            reverse("executabletasktype-list"),
            reverse("executabletasktype-create"),
            reverse(
                "executabletasktype-detail",
                kwargs={"pk": EXECUTABLE_TASK_TYPE_PK},
            ),
            reverse(
                "executabletaskinstance-create",
                kwargs={"pk": EXECUTABLE_TASK_TYPE_PK},
            ),
            reverse(
                "executabletasktype-delete",
                kwargs={"pk": EXECUTABLE_TASK_TYPE_PK},
            ),
            reverse(
                "executabletasktype-update",
                kwargs={"pk": EXECUTABLE_TASK_TYPE_PK},
            ),
            reverse("queue-list"),
            reverse("queue-create"),
            reverse("queue-detail", kwargs={"pk": TASK_QUEUE_PK}),
            reverse("queue-delete", kwargs={"pk": TASK_QUEUE_PK}),
            reverse("queue-update", kwargs={"pk": TASK_QUEUE_PK}),
            reverse("whitelist-list"),
            reverse("whitelist-create"),
        ]

        # Iterate over each page and make sure it's okay
        for page in pages_to_get:
            get_response = self.client.get(page)
            self.assertEqual(get_response.status_code, status.HTTP_200_OK)
