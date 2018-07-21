"""Contains tests for the splash page."""

from django.test import Client, TestCase
from django.urls import reverse
from splashpage.views import splash_page_view


class SplashPageIndexTestCase(TestCase):
    """Make sure the main page loads correctly."""
    def test_index(self):
        """Make sure we get a 200 when we hit the index page."""
        # Set up the client
        client = Client()

        # Find the URL to hit
        index_url = reverse(splash_page_view)

        # Hit the index page
        response = client.get(index_url)
        self.assertEqual(response.status_code, 200)
