from django.test import TestCase
from django.urls import reverse
from portfolio.models import PortfolioProject, Technology

class PortfolioViewsTests(TestCase):
    def setUp(self):
        # Create some Technology objects.
        self.tech1 = Technology.objects.create(
            name='Django',
            background_colour='092E20',
            text_color='FFFFFF'
        )
        self.tech2 = Technology.objects.create(
            name='Python',
            background_colour='306998',
            text_color='FFD43B'
        )

        # Create a complete project.
        self.complete_project = PortfolioProject.objects.create(
            title="Complete Project",
            short_description="A completed project",
            content="## This is a complete project\nSome **bold** text.",
            meta_description="Complete project meta description",
            meta_keywords="complete, project",
            is_complete=True,
            is_published=True,
        )
        self.complete_project.technologies.set([self.tech1, self.tech2])

        # Create an incomplete project.
        self.incomplete_project = PortfolioProject.objects.create(
            title="Incomplete Project",
            short_description="An upcoming project",
            content="## This is an incomplete project\nMore content here.",
            meta_description="Incomplete project meta description",
            meta_keywords="incomplete, project",
            is_complete=False,
            is_published=True,
        )
        self.incomplete_project.technologies.set([self.tech1])

        # Create additional projects to test pagination.
        # Total projects count: complete + incomplete + additional = 13 projects.
        self.additional_projects = []
        for i in range(1, 12):  # Creates 11 projects.
            project = PortfolioProject.objects.create(
                title=f"Project {i}",
                short_description=f"Short description {i}",
                content="Some **bold** content",
                meta_description=f"Meta {i}",
                meta_keywords="test, portfolio",
                is_complete=True,
                is_published=True,
            )
            project.technologies.set([self.tech1])
            self.additional_projects.append(project)

    def test_portfolio_list_view_template(self):
        """
        Test that the portfolio list view uses the correct template.
        """
        url = reverse('portfolio:portfolio')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/project_list.html')

    def test_portfolio_list_view_context_and_pagination(self):
        """
        Test that the list view returns projects in context and that pagination works.
        """
        url = reverse('portfolio:portfolio')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # 'projects' should be in context.
        self.assertIn('projects', response.context)
        projects = response.context['projects']

        # Since paginate_by is 10, the first page should have at most 10 projects.
        self.assertLessEqual(len(projects), 10)

        # Test the second page.
        response_page2 = self.client.get(url, {'page': 2})
        self.assertEqual(response_page2.status_code, 200)
        projects_page2 = response_page2.context['projects']
        # Total projects: 13 → page 1: 10 projects, page 2: 3 projects.
        self.assertEqual(len(projects_page2), 3)

    def test_portfolio_detail_view_complete_project(self):
        """
        Test that a complete project detail view renders correctly.
        """
        url = reverse('portfolio:project_detail', kwargs={'slug': self.complete_project.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/project_detail.html')

        # Check that the project title appears in the response.
        self.assertContains(response, self.complete_project.title)

        # Check that the rendered Markdown content appears in the response.
        rendered_content = self.complete_project.render_markdown_content()
        self.assertIn(rendered_content.strip(), response.content.decode())

        # Verify that the technology names are rendered.
        for tech in self.complete_project.technologies.all():
            self.assertContains(response, tech.name)

    def test_portfolio_detail_view_incomplete_project_redirect(self):
        """
        Test that an incomplete project detail view redirects to the portfolio list.
        """
        url = reverse('portfolio:project_detail', kwargs={'slug': self.incomplete_project.slug})
        response = self.client.get(url)
        # Since the project is incomplete, the view should redirect.
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = reverse('portfolio:portfolio')
        self.assertEqual(response.url, expected_redirect_url)
