# Step Four: Creating a basic blog

:warning: **Do not change any of the identifiers** (model or field names) in the given code snippets, or the data import script we offer to speed up the process of creating your demo blog pages will not work.

---

Now that you've extended the Home page and added some custom models that we'll need, we're going to work on building out a blog. We provided a foundation in the template to save some time, so let's head over to the `blog` directory and have a look at what's inside it.


* * *
## :memo: A quick note on project structure :memo:
In Wagtail projects, it is generally a good idea to keep related models in separate apps because it makes it a little easier for you to manage changes that affect migrations. Also, it makes it a little easier to decide where to put new code or models. Some Wagtail developers like to use a "core" or "base" app for models that are used across their projects. Others prefer not to use that approach because it can make future migrations a little trickier to manage. Both approaches are valid! For this workshop though, we're using the separate app approach.

* * *

<br/>

 Navigate to `blog/models.py`. You'll find models for two new page types for your blog. Wagtail is a CMS that uses a tree structure to organize content. There are parent pages and child pages. The ultimate parent page by default is the Home page. All other page types branch off of the Home page. Then child pages can branch off of those pages too.

The first page type you'll see is a parent type for the blog called `BlogPageIndex`. You don't have to use `Index` in the name but most Wagtail developers use that convention because it helps keep things organized. Here's what the code for `BlogPageIndex` looks like:

```python
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    subpage_types = ['blog.BlogPage']
```

This is a very simple version of `BlogIndexPage`. You'll be adding a few more things to it later, but this will work right now for getting your blog set up. We also added a setting called `subpage_type` that will link `BlogIndexPage` to a specific child page type. It's unlikely that blog editors will be creating any other page types connected to `BlogIndexPage`, so adding this setting improves their user experience by reducing the number of clicks they have to make to set up a page.

The second page type in the file is called `BlogPage`. The code looks like this:

```
class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    parent_page_types = ['blog.BlogIndexPage']
```


Think about the fields you typically need for a reader to enjoy a blog post. The title is included in a Wagtail model by default, so what else is usually needed? Blogs can get pretty messy without dates to organize them, so we added a `date` field. We also added an `intro` field to help readers get a preview of what the blog post is about. Note that the `intro` field has a `max_length` setting to keep editors from being too longwinded. A `body` field is pretty key for a blog too because otherwise there isn't a place to put any of your content. We're also added the `parent_page_type` setting to link `BlogPage` to `BlogIndexPage`.

```python
class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    parent_page_types = ['blog.BlogIndexPage']
```

## Making fields searchable

You're probably wondering what this chunk of code in `BlogPage` does:

```
search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
```

This code is telling Wagtail which fields you would like to be searchable. For the most part, you want users to be able to search as many fields as possible to help them find what they need. But there are some occassions where you don't want content to be indexed in the website search.

## 

## Adding Wagtail StreamField

One of the best parts of Wagtail is [StreamField](https://docs.wagtail.org/en/stable/topics/streamfield.html). StreamField gives users the power to mix and match different "blocks" of content rather than having a strict structure for a page. For example, someone writing a blog post could add a "quote" block to highlight a particular quote or phrase from their post. Or they could add a "sidebar" block that includes a little extra bonus content on the page. There aren't many limits to the types of blocks you can create.

To show you StreamField in action, you're going to create a simple StreamField implementation in the blog post `body` using some of the [default blocks](https://docs.wagtail.org/en/stable/reference/streamfield/blocks.html?highlight=blocks) that come with Wagtail. First, update your import statements in your `models.py` file so they look like this:

```python
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.embeds.blocks import EmbedBlock
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
```

Then, at the top of the file under the imports, add this one custom block that we'll start with:

```python
class HeadingBlock(blocks.StructBlock):
    size = blocks.ChoiceBlock(
        choices=[
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
    )
    text = blocks.CharBlock()

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"
```

Next, replace the `body` definition from `RichTextField` in your `BlogPage` class with the following code:

```python
    body = StreamField(
        [
            ("heading", HeadingBlock()),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("embed", EmbedBlock(max_width=800, max_height=400)),
        ]
    )
```

Your whole file should now look like this:

```python
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.embeds.blocks import EmbedBlock
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class HeadingBlock(blocks.StructBlock):
    size = blocks.ChoiceBlock(
        choices=[
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
    )
    text = blocks.CharBlock()

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    subpage_types = ['blog.BlogPage']


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField(
        [
            ("heading", HeadingBlock()),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("embed", EmbedBlock(max_width=800, max_height=400)),
        ]
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    parent_page_types = ['blog.BlogIndexPage']
```

Save your file and then run the migration commands `python manage.py makemigrations` and `python manage.py migrate`. Start up the development server real quick with `python manage.py runserver` then have a look at a blank Blog Page. You'll notice that the "body" section now has a green plus sign in it. When you click on it, a collection of blocks will appear for you to choose from. You can experiment with combining blocks if you want to.

## Load some demo pages

Rather than creating your own blog index and blog pages, it might be easier to run a script to load these into your database. Running our script will also help by ensuring that you have an example accessibility issue that we'll look at later.

Copy the contents of [`/blog/mangement/commands/seed_data.py`](https://github.com/vossisboss/pyconwagtail2024/blob/step-4/blog/management/commands/seed_data.py) from this branch and paste it in the same location in your project. Then run `python manage.py seed_data` to load up our demo Blog Index Page and a child Blog Page. After it completes, refresh the Wagtail admin to see the new pages there.

---

TODO:

- [x] Add section where we load initial content via fixture to ensure people see the accessibility issues we want to demonstrate.
  - [x] Add note to earlier sections to make sure people don't change any of the names in the same code, or the fixture won't work.
- [ ] Incorporate CSS and (some?) HTML into new project template that gets brought in with `wagtail start` in step 1
  - [ ] Make a couple intentional accessibility errors along the lines of what Scott fixes in the Bakery Demo during his DjangoCon talk (but don't call attention to them in this README)
- [ ] Add "Adding templates for your blog pages" section from previous tutorial's Step 4 for any HTML bits we didn't include in the project template
- [ ] End this step by viewing the frontend with our imported content
