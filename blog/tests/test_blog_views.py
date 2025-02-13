from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from blog.models import Post, Category

User = get_user_model()


class BlogViewsTest(TestCase):
    def setUp(self):
        # Create a test user.
        self.user = User.objects.create_user(
            username='testuser', password='password'
        )

        # Create two categories.
        self.category1 = Category.objects.create(
            name='Test Category',
            background_colour='000000',
            text_color='ffffff',
            slug='test-category'
        )

        self.category2 = Category.objects.create(
            name='Another Category',
            background_colour='111111',
            text_color='eeeeee',
            slug='another-category'
        )

        self.post1 = Post.objects.create(
            title='First Post',
            slug='first-post',
            category=self.category1,
            author=self.user,
            excerpt='First excerpt',
            content='Content for **first** post.',
            hashtags='Python, Django',
            meta_description='Meta description 1',
            meta_keywords='keyword1, keyword2',
            alt_text='Alt text 1',
            created=timezone.now(),
        )
        self.post2 = Post.objects.create(
            title='Second Post',
            slug='second-post',
            category=self.category2,
            author=self.user,
            excerpt='Second excerpt',
            content='Content for *second* post.',
            hashtags='Testing, Django',
            meta_description='Meta description 2',
            meta_keywords='keyword3, keyword4',
            alt_text='Alt text 2',
            created=timezone.now(),
        )

        for i in range(3, 9):
            Post.objects.create(
                title=f'Post {i}',
                slug=f'post-{i}',
                category=self.category1,
                author=self.user,
                excerpt=f'Excerpt for post {i}',
                content=f'Content for post {i}',
                hashtags='Test, Django',
                meta_description=f'Meta description {i}',
                meta_keywords='test, django',
                alt_text=f'Alt text {i}',
                created=timezone.now(),
            )

    def test_post_list_view_template(self):
        """
        Test that the list view uses the correct
        template for a normal request.
        """
        url = reverse('blog:post_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_list_view_htmx_template(self):
        """Test that an HTMX request returns the partial template."""
        url = reverse('blog:post_list')
        # HTMX requests include the header 'HX-Request': 'true'
        response = self.client.get(url, HTTP_HX_REQUEST='true')
        self.assertTemplateUsed(
            response, 'blog/partials/post_list_partial.html'
        )

    def test_post_list_view_filter_by_category(self):
        """
        Test that filtering by category returns
        only posts from that category.
        """
        url = reverse('blog:post_list')
        response = self.client.get(url, {'category': 'test-category'})
        self.assertEqual(
            response.context.get('selected_category'), 'test-category'
        )
        # All returned posts should belong to category1.
        for post in response.context['posts']:
            self.assertEqual(post.category.slug, 'test-category')

    def test_post_list_view_search_filter(self):
        """Test that the search query filters posts appropriately."""
        url = reverse('blog:post_list')
        response = self.client.get(url, {'search': 'First'})
        posts = response.context['posts']
        self.assertTrue(any('First' in post.title for post in posts))
        for post in posts:
            title_match = 'first' in post.title.lower()
            hashtags_match = 'first' in post.hashtags.lower()
            category_match = 'first' in post.category.name.lower()
            self.assertTrue(title_match or hashtags_match or category_match)

    def test_post_list_view_context_categories(self):
        """Test that the list view context includes the categories."""
        url = reverse('blog:post_list')
        response = self.client.get(url)
        self.assertIn('categories', response.context)
        categories = response.context['categories']
        self.assertIn(self.category1, categories)
        self.assertIn(self.category2, categories)

    def test_post_list_view_pagination(self):
        """Test that pagination limits the number of posts per page."""
        url = reverse('blog:post_list')
        response = self.client.get(url)
        # number of posts in the context dosen't exceed 5.
        self.assertLessEqual(len(response.context['posts']), 5)

    def test_post_list_view_second_page(self):
        """
        Test that the second page of pagination returns
        the remaining posts.
        """
        url = reverse('blog:post_list')
        response = self.client.get(url, {'page': 2})
        self.assertEqual(response.status_code, 200)
        # Total posts created: 8. First page 5 posts, second page 3.
        self.assertEqual(len(response.context['posts']), 3)

    def test_post_detail_view_context(self):
        """
        Test that the detail view includes rendered markdown,
        formatted hashtags, and related posts.
        """
        url = reverse('blog:post_detail', kwargs={'slug': self.post1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check for rendered Markdown content.
        self.assertIn('rendered_content', response.context)
        rendered_content = response.context['rendered_content']
        self.assertIn('<p>', rendered_content)

        # Check that hashtags are correctly formatted.
        self.assertIn('formatted_hashtags', response.context)
        formatted_hashtags = response.context['formatted_hashtags']
        self.assertEqual(formatted_hashtags, ['#python', '#django'])

        # Check related posts are present and doon't include the current post.
        self.assertIn('related_posts', response.context)
        related_posts = response.context['related_posts']
        for post in related_posts:
            self.assertNotEqual(post.id, self.post1.id)
            self.assertEqual(post.category, self.post1.category)
