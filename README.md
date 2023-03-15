# Step Four: Add Blog models and content

Having one home page really isn't enough for a blog. We need to add some more pages and content to our site so we have some content to translate.

Now that you've extended the Home page and added some useful fields, let's add the key parts of our blog. To do that, you'll need to create a new app with the command:

```
python manage.py startapp blog
```

Then you need to add that app to `INSTALLED_APPS` in `myblog/settings/base.py`:

```
INSTALLED_APPS = [
    "home",
    "search",
    # Insert this
    "blog",
    "wagtail_localize",
    "wagtail_localize.locales",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    # ...
]
```
<br/>

* * *
## :memo: A quick note on project structure :memo:
In Wagtail projects, it is generally a good idea to keep related models in separate apps because it makes it a little easier for you to manage changes that affect migrations. Also, it makes it a little easier to decide where to put new code or models. Some Wagtail developers like to use a "core" or "base" app for models that are used across their projects. Others prefer not to use that approach because it can make future migrations a little trickier to manage. Both approaches are valid! For this tutorial though, we're going to use the separate app approach.

* * *

<br/>

Now that you have a blog app added to your project, navigate to `blog/models.py`. We're going to create two new page types for our blog. Wagtail is a CMS that uses a tree structure to organize content. There are parent pages and child pages. The ultimate parent page by default is the Home page. All other page types branch off of the Home page. Then child pages can branch off of those pages too.

First, you need to create a parent type for the blog. Most Wagtail developers will call these pages "index" pages, so this one will be called `BlogPageIndex`. Add the following code to your `models.py` file in the blog app:

```

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
```

This is a very simple version of `BlogIndexPage` with only a single `intro` field to describe the blog. You'll be adding a few more things to it later, but this will work right now for getting your blog set up.

Next, we need to create a child page called `BlogPage`. Add the following code beneath `BlogIndexPage`:

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
```

Your whole file should now look like this:

```
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

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
```

Save all of your work. Then run `python manage.py makemigrations` and `python manage.py migrate`.

## Add some blog content

Let's run the development server with `python manage.py runserver`and add some content so we'll have something work with when we add templates for these pages. Go to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) and click the "Pages" menu then click "Badger Bonanza" (or whatever title you chose) to open the menu for that page. Click the three purple dots to open the action menu and click "Add child page". Choose the "Blog index page" this time.

![Screen shot of action menu from home page](https://www.meagenvoss.com/media/images/Screen_Shot_2022-09-28_at_9.04.21_PM.original.png)

 Fill out the title and intro line for your blog. I used the oh-so-creative title "Blog" and "The latest badger sightings" if you would like to steal those brilliant lines. Use the big green button at the bottom to "Publish" the page.

Back in the "Badger Bonanza" section of Wagtail, you should now see a line for your "Blog" page. When you hover over "Blog", a button should appear that says "Add child page." Click the button. Pick "Blog page".

![Screenshot of the Blog page in the list](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-03_at_3.47.11_PM.original.png)

Fill out some content on your blog page. If your creative muse has deserted you to sip margharitas on a beach, then you can add today's date, use the title "Badgers are brilliant" and the intro line "We have totally underestimated badgers".

You can play with the body right now if you like. HOWEVER, make sure the body field is completely blank BEFORE you publish your page. If it is NOT blank, you will run into a database error during the migration in the next step.

Again, make sure your body field is *completely blank* before proceeding. Then use the big green button at the bottom of the page and click "Publish".

## Adding Wagtail StreamField

You can do a lot with the body of your Blog page the way it is currently set. You can add images and embedded videos and some different formatting. But sometimes content creators need more than those features. That's where the power of [Wagtail StreamField](https://docs.wagtail.org/en/stable/topics/streamfield.html) comes into play.

StreamField gives users the power to mix and match different "blocks" of content rather than having a strict structure for a page. For example, someone writing a blog post could add a "quote" block to highlight a particular quote or phrase from their post. Or they could add a "sidebar" block that includes a little extra bonus content on the page. There aren't many limits to the types of blocks you can create.

To show you StreamField in action, you're going to create a simple StreamField implementation in the blog post `body` using some of the [default blocks](https://docs.wagtail.org/en/stable/reference/streamfield/blocks.html?highlight=blocks) that come with Wagtail. First, add these import statements to your `models.py` file:

```
from wagtail.fields import StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
```

Next, we need to modify the `body` definition a bit because we have data already stored in our blog body. Update the `body` definition so that it is:

```
body = RichTextField(blank=True, null=True)
```
Then run:

```
python manage.py makemigrations
python manage.py migrate
```

Next, replace the `body` definition from `RichTextField` in your `BlogPage` class with the following code:

```
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock(max_width=800, max_height=400)),
    ], use_json_field=True)
```

Save your file and then run the migration commands `python manage.py makemigrations` and `python manage.py migrate`. Start up the development server real quick with `python manage.py runserver` then have a look at a blank Blog Page. You'll notice that the "body" section now has a row of blocks for you to choose from.

Re-enter your body content now. If you're feeling low on inspiration, add a Paragraph block with:

```
Here are three reasons badgers are more intelligent than we thought they were:

    1. They use tools
    2. They can solve puzzles
    3. They can break out of zoos

```

And then an embed block with this URL for the glorious Internet classic "Badger, Badger, Badger": `https://www.youtube.com/watch?v=EIyixC9NsLI`

Next, click the big green button at the bottom of the page and click "Publish".

<br />

***

## :warning: Be aware of custom models :warning:

Before we move on, I want to call attention to one major quirk of Django and Wagtail : custom models. In the Django documentation, it says "It’s highly recommended to set up a custom user model, even if the default User model is sufficient for you." This is because creating a custom user model in the middle of a project or with an existing database is a huge hassle. Even very smart people haven't figure out how to create a migration fix for it yet. The Django ticket to solve this issue has been open for years.

To save some time, we're not going to add custom models to our Wagtail project in this workshop. If you want to add the models afterwards, here are the key models you should consider creating custom models for and links to the appropriate documentation:

- [User](https://docs.wagtail.org/en/stable/advanced_topics/customisation/custom_user_models.html#custom-user-models)
- [AbstractImage and AbstractRendition](https://docs.wagtail.org/en/stable/advanced_topics/images/custom_image_model.html#custom-image-model)
- [AbstractDocument](https://docs.wagtail.org/en/stable/advanced_topics/documents/custom_document_model.html#id1)

## Adding templates for your blog pages

Now that you entered some content, let's create some templates to go with it. First, go to `myblog/templates` and create a directory labeled `blog`. In that `blog` directory, create two blank files: `blog_index_page.html` and `blog_page.html`

In `blog_index_page.html`, let's add:

```
{% extends "base.html" %}

{% load wagtailcore_tags %}

{% block body_class %}template-blogindexpage{% endblock %}

{% block content %}
    <h1>{{ page.title }}</h1>

    <div class="intro">{{ page.intro|richtext }}</div>

    {% for post in page.get_children %}
        <h2><a href="{% pageurl post %}">{{ post.title }}</a></h2>
        {{ post.specific.intro }}
        {{ post.specific.body }}
    {% endfor %}

{% endblock %}
```

Save that file and then add the following code to `blog_page.html`:

```
{% extends "base.html" %}

{% block body_class %}template-blogpage{% endblock %}

{% block content %}
    <h1>{{ page.title }}</h1>
    <p class="meta">{{ page.date }}</p>

    <div class="intro">{{ page.intro }}</div>

    {{ page.body }}

    <p><a href="{{ page.get_parent.url }}">Return to blog</a></p>

{% endblock %}
```

Excellent! Now you have some basic templates for your blog content in English that you can work with. Let's have a quick look at your content by checking that it works. In the Wagtail admin, navigate to "Pages" then click "Badger Blog". You should see your "Blog" page listed like this:

![Screenshot of Wagtail showing Badger Blog listing](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-12_at_10.19.28_PM.original.png)

Hover over the "Blog" listing to make the buttons appear then click "View live" to see what your `BlogIndex` page looks like. You should be able to click on your blog article and open up your "Badgers are brilliant" blog then navigate back to your "Blog" page. The "Home" page and the "Blog" page aren't connected yet. Don't worry, we'll get there.


