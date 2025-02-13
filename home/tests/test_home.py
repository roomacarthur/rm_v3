from django.test import TestCase
from django.urls import reverse, resolve
from home.views import Home


class HomeTests(TestCase):
    """Tests for the Home view."""

    def test_home_view_status_code(self):
        """Test that the home view returns a 200 status code."""
        url = reverse('home:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        """Test that the home URL resolves to the Home view."""
        view = resolve('/')
        self.assertEqual(view.func.view_class, Home)

    def test_home_view_uses_correct_template(self):
        """Test that the home view uses the correct template."""
        url = reverse('home:home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_home_view_contains_correct_html(self):
        """Test that the home view contains the correct HTML."""
        url = reverse('home:home')
        response = self.client.get(url)
        self.assertContains(response, "Hey it's Roo!")

    def test_home_view_does_not_contain_incorrect_html(self):
        """Test that the home view does not contain incorrect HTML."""
        url = reverse('home:home')
        response = self.client.get(url)
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.'
        )
