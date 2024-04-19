from django.core.management.base import BaseCommand

from wagtail.models import Page

from blog.models import BlogIndexPage, BlogPage


class Command(BaseCommand):
    help = "Create initial blog data"

    def handle(self, *args, **options):
        # Create a blog index page instance
        blog_index = BlogIndexPage(
            title="Demo Blog Index",
            slug="demo-blog-index",
            intro="Welcome to my blog!",
            live=True,
        )
        # Add it as a child of the homepage
        home = Page.objects.get(pk=3)
        home.add_child(instance=blog_index)

        # Create blog page instances
        blog_page = BlogPage(
            title="Hello, world!",
            slug="hello-world",
            date="2024-01-01",
            intro="This is my first blog post.",
            body='[{"type": "heading", "value": "Heading Block heading", "id": "87964bfb-bf30-4bc8-b569-7acd3a14bf9b"}, {"type": "paragraph", "value": "<p data-block-key=\\"79s93\\">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p><h4 data-block-key=\\"dhpsv\\">Heading level 4 within RTB</h4><p data-block-key=\\"7smvs\\">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", "id": "b819273e-8f80-46e1-a31a-405fbf5035f4"}]',
            live=True,
        )
        # Add it as a child of the blog index
        blog_index.add_child(instance=blog_page)

        print("✅ Blog data seeding complete!")
