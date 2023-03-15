# Step One: Set up Wagtail

## Create a virtual environment

### _Gitpod_

If you don't have Python already installed on your machine or if you would prefer not to troubleshoot environment issues, then you can complete this workshop in Gitpod. You will have to be more careful about saving your work since Gitpod environments deactivate after a period of inactivity.

Click the button below to launch Gitpod.

**NOTE**: A GitHub account is required to use Gitpod

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/vossisboss/pvdjango-gitpod)

### _Venv_

If you already have Python installed on your machine, you can create a local virtual environment using `venv`. Open your command line and navigate to the directory you want to build your project in. Then enter the following commands to creative a virtual environment.

```
python 
python -m venv env
source env/bin/activate
```

## Set up Wagtail

Once you have a virtual environment set up, we can install Wagtail and start setting up our very first Wagtail website. In your project directory, enter the following command in your command line:

```
pip install wagtail
```

This command tells the Python package manager pip to install the latest release of Wagtail along with all of the dependencies that are needed for Wagtail. After Wagtail is installed, you can confirm that it is installed with:

```
pip show wagtail
```

After Wagtail is installed, you can use one of Wagtail's built-in commands to start a brand new website. For this tutorial, we're going to be creating a mini-blog project called `myblog`.

```
wagtail start myblog .
```

Don't forget the `.` at the end of the command. It is telling Wagtail to put all of the files in the current working directory.

Once all of the files are set up, you'll need to enter some commands to set up the test database and all of the migration files that Wagtail needs. You can do that with the `migrate` command.

```
python manage.py migrate
```

After the migrations are complete, you'll need to create a superuser so that you can access the backend of your Wagtail website. Use the following command:

```
python manage.py createsuperuser
```
Follow the prompts in your command line to create your superuser. Once you have a superuser set up, you can start up the test server to see your new Wagtail site in action.

```
python manage.py runserver
```
If the server has started up without any errors, you can navigate to [http://127.0.0.1:8000 ](http://127.0.0.1:8000 ) in your web browser to see your Wagtail website. If you've successfully installed Wagtail, you should see a home page with a large teal egg on it.

To test that your superuser works, navigate to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) and login with the credentials you created.

Now you have a basic Wagtail website set up. Next, we're going to add a package that will help you organize and translate content across different languages and locales.

<br />

* * *

## :memo: A quick note for Gitpod users :memo:

To log into the Wagtail backend, you're going to have to add a line of code to your `dev.py` file in settings. Navigate to `myblog/settings/dev.py` and add the following line of code to your file:

```
CSRF_TRUSTED_ORIGINS = ['https://*.gitpod.io']
```
<br />

# Step Two: Install and configure Wagtail Localize

Wagtail Localize is a package that will help you set up a translation workflow for your website. It provides a few different options for translation workflows, but one of the most useful features is the ability to sync content from the main language to other languages.


## Install the Wagtail Localize package

 To install Wagtail Localize, enter the following command in your command line:

```
pip install wagtail-localize
```

With that update in place and the package installed, now you are going to make some changes to `base.py` and `urls.py`. Most of the steps you're going to perform next come from the [Wagtail Localize documentation](https://www.wagtail-localize.org/). 


## Add Wagtail Localize to INSTALLED_APPS


Go to `myblog\settings\base.py` and open the file in your text editor or IDE. Find the `INSTALLED_APPS` setting, and insert `'wagtail_localize'` and `'wagtail_localize.locales'` in between
`'search` and `'wagtail.contrib.forms'`:

```python
INSTALLED_APPS = [
    "home",
    "search",
    # Insert these here
    "wagtail_localize",
    "wagtail_localize.locales",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    # ...
]
```

Note that the `wagtail_localize.locales` module is a temporary replacement for Wagtail's builtin `wagtail.locales`
module.

## Enable internationalization in Wagtail

Find the "Internationalisation" section, and add the `WAGTAIL_I18N_ENABLED` setting:

```python
USE_I18N = True

USE_L10N = True

# Add this
WAGTAIL_I18N_ENABLED = True

USE_TZ = True
```

## Configure languages


In the "Internationalisation" section, add the following to set the `LANGUAGES` and `WAGTAIL_CONTENT_LANGUAGES`
settings to English and French:

```python
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ("en", "English"),
    ("fr", "French"),
]
```

## Add machine translation configuration

Wagtail Localize has a few different options for machine translation. Two available integration options include Google Cloud Translation and Deepl. Both of those options require setting accounts up with credit cards, so we're going to use a dummy translator for this tutorial to show you how things work. If you want to integrate a machine translator later on, you can follow the steps in the [Wagtail Localize Documentation](https://www.wagtail-localize.org/how-to/integrations/machine-translation/) to add the configuration for your preferred translator to `base.py`. There is also an integration available for [Pontoon](https://www.wagtail-localize.org/how-to/integrations/pontoon/).

To add the dummy translator, add the following code to your `base.py` file:

```
WAGTAILLOCALIZE_MACHINE_TRANSLATOR = {
    "CLASS": "wagtail_localize.machine_translators.dummy.DummyTranslator",
}
```

## Enable `LocaleMiddleware`

Django's `LocaleMiddleware` detects a user's browser language and forwards them to the most appropriate language
version of the website.

To enable it, insert `"django.middleware.locale.LocaleMiddleware"` into the middleware setting
above `RedirectMiddleware`:

```python
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # Insert this here
    "django.middleware.locale.LocaleMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]
```
## Configure URL paths

Next, you need configure which URL paths are translatable so that Django will prefix them with the language code.

Open `myblog/urls.py`. You'll see that there are two groups of URL patterns with an
`if settings.DEBUG:` block in between them.

The patterns that need to be made translatable are:

- `path('search/', search_views.search, name='search'),`
- `path("", include(wagtail_urls)),`

To make these translatable, move the 'search/' pattern into the second block, above the `wagtail_urls` pattern. Then,
replace the square brackets around that block with
[`i18n_patterns`](https://docs.djangoproject.com/en/3.1/topics/i18n/translation/#django.conf.urls.i18n.i18n_patterns):

```python
from django.conf.urls.i18n import i18n_patterns


# These paths are translatable so will be given a language prefix (eg, '/en', '/fr')
urlpatterns = urlpatterns + i18n_patterns(
    path("search/", search_views.search, name="search"),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
)
```

With the search pattern removed, the first group should now look like:

```python
# These paths are non-translatable so will not be given a language prefix
urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
]
```

At this point, you might want to take a quick peak at the `urls.py` file in the [step-2](https://github.com/vossisboss/pvdjango/tree/step-2) branch to make sure they match. This step can be a little tricky.

## Migrate the database

Run the migrate command again to set up the tables for Wagtail Localize in the database:

```
python manage.py migrate
```

## Check your site


Go back to [http://127.0.0.1:8000](http://127.0.0.1:8000). If your browser is configured for English or any other language except French,
you should be redirected to [http://127.0.0.1:8000/en](http://127.0.0.1:8000/en).
If your browser is configured in French, you should be redirected to [http://127.0.0.1:8000/fr](http://127.0.0.1:8000/fr).

In either case, you can view the site in `/en/` or `/fr/` (no differences yet).

If this is all working as described, that means `i18n_patterns` and `LocaleMiddleware` are working!

# Step Three: Extend the home page model

Before you start adding content and translating it, you'll need to add some models to Wagtail. Wagtail models are derived from [Django models](https://docs.djangoproject.com/en/4.1/topics/db/models/). One key difference in writing models for Wagtail is that adding views isn't necessary unless you need to create a highly customized view or form. We'll go over this in a bit more detail when you add templates to your project. For right now, you mostly need to know that models provide the essential fields and structures for the content on your Wagtail site that will be stored in your database.

Many of the steps you'll be doing here have been borrowed from the [Getting Started tutorial](https://docs.wagtail.org/en/stable/getting_started/tutorial.html) for Wagtail.

## Extending the `HomePage` model

Right out of the box, Wagtail comes with a `home` app that provides a blank `HomePage` model. This model will define the home page of your website and what content appears on it. Go to the `home` directory in your project and open up `models.py`. You'll see that all the model currently has in it by default is a `pass` command. So you're going to have to extend it to add content to your home page.

 Since this is a blog site, you should probably tell your readers what the blog is about and give them a reason to read it. All pages in Wagtail have a title by default, so you'll be able to add the blog title easily. So let's extend the `HomePage` model by adding a text field for a blog summary to the model.

First, you'll need to add some additional import statements to the top of the page. This statement will import the `RichTextField` (one that lets you use bold, italics, and other formatting) from Wagtail:

```
from wagtail.fields import RichTextField
 ```

And this statement will import the panel you need to make sure your new field appears in the Wagtail admin as well:

```
from wagtail.admin.panels import FieldPanel
```

Once those import statements are added, delete `pass` from your `HomePage` model and replace it with:

```
summary = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
    ]

```

Your whole file should look like this right now:

```

from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    summary = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
    ]
```

Awesome! So what else do we need to have an attractive home page for the blog? An image is something most readers find appealing, so let's add an image to the `HomePage` model as well. Add the following code beneath your `summary` variable:

```
main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
```

And then add another line to `content_panels`:
```
FieldPanel('main_image'),
```

Your full `models.py` file should like like this now:

```
from dataclasses import Field
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    summary = RichTextField(blank=True)
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        FieldPanel('main_image'),
    ]

```

Now you have fields for a summary and for adding an image to your home page. To add those fields to the database, run the following migration commands:

```
python manage.py makemigrations
python manage.py migrate
```

## Check your fields with the development server 

Let's get the development server up and running in your terminal with:

```
python manage.py runserver
```
Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to check that your homepage is still functional. Then navigate to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to access the admin log in page. Log in with the superuser you created in Step One.

Now you're in the Wagtail dashboard. You'll see lots of handy stuff like a list of the number of pages, your latest revisions, and other useful things. On the left hand side is the main toolbar for Wagtail. Select "Pages" from this toolbar and then click the "Home" link.

You'll be taking to Home parent page listing, which is pretty empty right now because there aren't any pages inheriting from the Home page yet. Click the three little dots next to "Home" at the top of the page to open the action menu. Choose "Edit".

Now we're going to add some data to our blog. Feel free to choose your own theme. But if you're not feeling particularly inspired, you can join me in filling out "Badger Bonanza" for the title and "Musings on Earth's most noble and distinctive mammal" for the summary. You'll need a picture too. Feel free to use this [lovely badger](https://upload.wikimedia.org/wikipedia/commons/4/41/M%C3%A4yr%C3%A4_%C3%84ht%C3%A4ri_4.jpg) from Wikimedia Commons. Click "Choose an image" and then upload the image to Wagtail.

![Screenshot of home page in Wagtail admin](https://www.meagenvoss.com/media/images/Screen_Shot_2022-09-28_at_9.16.11_PM.original.png)

When you're done adding the content, go to the bottom of the page and use the big green button to save your draft. Then click on the arrow next to "Save draft" to open up the publish menu and click "Publish" to publish the page.

![Screenshot of Wagtail publish button](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-05_at_11.56.07_PM.original.png)

Go ahead and click the "View Live" link when it comes up.

Oh no! There's no badger! Did we do something wrong? Nope. We have to remove the default homepage that came with Wagtail, so let's do that.

## Remove the default homepage

Go to `home/templates/home/home_page.html` and delete everything in the file except for the first line `{% extends "base.html" %}`. Update the file so it looks like this:

```
{% extends "base.html" %}
{% load wagtailcore_tags wagtailimages_tags %}

{% block body_class %}template-homepage{% endblock %}

{% block content %}

<h1>{{ page.title }}</h1>

<p>{{page.summary}}</p>

{% image page.main_image max-500x500 %}

{% endblock %}
```
Save the file and then reload your homepage. You should now see the title of your blog, the summary, and a beautiful badger (if you chose to go with my badger theme rather than your own).

Now, the summary might look a little funky. And that is because text fields do not print with escaped characters by default. Fortunately, Wagtail comes with a handy filter, among many other [handy filters](https://docs.wagtail.org/en/stable/topics/writing_templates.html#template-tags-and-filters), that can render the text properly. Update the `{{page.summary}}` line so that it is:

```
<p>{{page.summary|richtext}}</p>
```
Refresh the page and the summary text should be displaying properly now.

Before you move on from this task, let's clean your templates and organize things a bit. Navigate to `myblog\templates` and create a new directory in it called `home`. Move `home_page.html` to the new `home` directory. Refresh the page to make sure it still works. The delete the `templates` directory in the `home` app. While you're there, you can also delete the `static` folder in the the `home` app because all that is in it is some CSS for the default home page.

This structure will help you stay organized by keeping all of your templates in one directory. Trust me, any frontend developers you work with will thank you. And then they will find something else to pick on, but that's the way of things.

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


# Step Five: Translate your content

Let's work on translating the English content so that we have some content in French to work with as well. We're going to use `wagtail-localize` to help save time by syncing our content from the primary language of our blog.

## Setting up your new locale

To set up a locale for French, go to the lefthand menu, click "Settings", then click "Locales". On the righthand side, click the green "Add a locale" button. In the "Language" dropdown menu, choose "French". 

Beneath the dropdown is an option to synchronize content from the main language of your website. Click the green "Enable" button. Check the "Enabled" checkbox and then select "English" from the "Sync from" menu. Click "Save" to save your changes.

![Screenshot showing how to add a locale to Wagtail](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-03_at_4.21.46_PM.original.png)

Now click "Pages" on the lefthand menu and you'll see there are now _two_ versions of "Badger Blog." One says "English" next to it and the other says "French." Click on the "French" version of "Badger Blog" to edit it. You'll be presented with an option to translate the "Badger Blog" page and all of the pages in the subtree. Check the box to translate all of the pages. 

![Screenshot showing the translate subtree option in Wagtail](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-03_at_4.23.52_PM.original.png)

Now when you open the "Pages" menu, you should see two copies of your page trees: one labeled "English" and another labeled "French".

Click "Edit" for the French version of the "Badger Blog" Page to edit the content. The page will open up in a translation view. The translation view provides the content in the original language and provides you with some different options to translate it.

![Screenshot of the initial translation view for Badger Blog](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-13_at_6.58.01_AM.original.png)

## Translate using PO files

PO files are the file format used by professional translators for translating a variety of structured content, including websites. If you are going to be working with a living, breathing human translator, this could be a good option for your project. The advantages of the PO file is that everything can be translated in one file, and you can send that file to a translator without having to give them access to the admin section of your website.

To use the PO file method, click the "Download PO file" button to download the file. Then either send the file to a translator or use a program like [Poedit](https://poedit.net/download) to edit the file and translate it. Once the file has been translated, you can upload it to your page with the "Upload PO File" button.

Once the file is uploaded, check that there are green checkmarks throughout your page. Click the promote tab too and make sure the slug has been translated as well. Once everything is translated click the big green "Publish in French" button at the bottom to publish the page.

## Translate manually

You can also use the Wagtail Localize plugin to translate content manually as well. This approach is best to use if you decide you are okay with creating a log in for your translator or if someone who will be working on the website regularly is also translating the content. To do manually translation, go through each item on the page and click "Translate". Once you are done adding the translation, click "Save" to save your changes. Do this for each piece of content on the page. Click the "Promote" tab to translate the slug as well. Once you're done, click "Publish in French" at the bottom of the page to publish the page.

**NOTE** Be very careful of using quote marks in your translations. Quote marks in certain languages are different from the quote marks used in HTML. So if there are any links in your content, you need to make sure you're using the right type of quote marks in any HTML included in your translations.

## Machine translation

You can also hit the third button on the page to use the machine translation integration you set up earlier. Now since you set up the Wagtail Localize dummy translator, all it will do here is reverse all of the strings on the page. But it will give you an idea how Deepl or Google Cloud Translation would work if you set them up. If you use this option for your translation, you'll need to click back into the page and publish the results by clicking the "Publish in French" button.

## Translate and publish your pages

Using whichever method you prefer, go through and translate your "Blog" page as well as your "Badgers are brilliant" article. Be sure to publish each one of those pages after you finish adding your translations.

## Syncing content from your main language

Let's try syncing some changes from a blog written in your main language. In the lefthand menu, go to "Pages" then click the arrow to the right until you see "Badgers are brilliant". Play with the language switcher in the admin above it if you want to see how easy it is to switch between the languages. Click on the pencil to open the edit page for "Badgers are brilliant".

![Screenshot of an example of the admin language switcher](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-13_at_7.07.57_AM.original.png)


Scroll down to the body. You're going to add the link to this [YouTube video](https://www.youtube.com/watch?v=c36UNSoJenI) about an escape artist badger to the line "They can break out of zoos." Add the link by highlighting the text and selecting the link option from the menu. When the link menu pops up, click "External link" to add the link to text.

Publish the page with the new changes. After you hit Publish, you'll be returned to the menu for the "Blog" parent page. Hover over "Badgers are brilliant" and click the "More" button. Select "Sync translated pages."

![Screenshot of syncing translated pages](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-03_at_5.17.00_PM.original.png)

After you set up the sync, navigate to the French version of the page. Your changes to the content will be highlighted in yellow and you can translate them or insert local content. Notice how links and images are separated from the text and can be changed to make them more appealing to a French audience. For example, if you wanted to include a link to a video that was in French or that had French subtitles switched on, you could include a unique link in the French version of the blog. You're welcome to try this by including a link to a different video in the French version. Perhaps this video on [European badgers](https://www.youtube.com/watch?v=PvpNx0Hxtdk) would be more appropriate for your French audience.

All right. Now that we've added some content to your blog and translated it into French, we're going to add a translatable menu and a translatable footer to our website so that you can see how Snippets work in Wagtail as well as how you can translate them.


# Step Six: Add translatable navigation

In this step, you're going to learn about Wagtail Snippets. Snippets are pieces of code that can be used in multiple places across a project but that aren't a part of the page tree. Some common uses for Snippets include author profiles, menus, and footer content. The nice thing about Wagtail is you can use `TranslatableMixin` to make your snippets translatable by Wagtail Localize.

## Add a navigation app

To follow the separate apps structure, you're going to create a new app for all of the pieces related to website navigation. To create the app, type the following command into your terminal:

```
python manage.py startapp navigation
```

You'll need to update your `INSTALLED_APPS` in `myblog/settings/base.py` so that the top of it looks like this:

```
INSTALLED_APPS = [
    "home",
    "search",
    "blog",
    "navigation",
    "wagtail_localize.locales",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    # ...
]
```

You'll use this app to store the models related to your translatable navigation snippets as well as some template tags that we'll use to help display the correct text for each locale. Curious what template tags are? You'll find out soon.

## Add a model for a translatable navigation menu

We're going to add a translatable main navigation menu at the top of the page so you make sure the pages you want to display specifically for each locale appear in the menu.

First, let's add some import statements to `navigation/models.py`:

```
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.models import TranslatableMixin
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import PageChooserPanel

```

You'll need `TranslatableMixin` to make your menu translatable, `FieldPanel` and `PageChooserPanel` to add the panels you need to the admin interface, and `register_snippet` to add this model as a Snippet rather than a Wagtail page model. Here's how you will set up the Snippet:

```
@register_snippet
class MainNavigation (TranslatableMixin, models.Model):
    name = models.CharField(max_length=255)

    menu_page = models.ForeignKey(
          'wagtailcore.Page',
          null=True,
          blank=True,
          on_delete=models.SET_NULL,
          related_name='menu_page'
      )

    panels = [
        FieldPanel("name"),
        PageChooserPanel('menu_page'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Main navigation"
        unique_together = [
            ("translation_key", "locale"),
        ]

```

Let's look at the different pieces. In setting up the class, you're telling `MainNavigation` to call on `TranslatableMixin` and `models.Model`. In the next lines, you're creating a field called `name` and you are creating a `menu_page` field with a `ForeignKey` that allows you to access all existing `Page` models on your website. Then we're telling Wagtail to offer two panels for managing those models.

The `PageChooserPanel` is a Wagtail feature that brings up a handy page selecter menu. That way, users can select from existing pages without having to re-enter a bunch of information. It's a very useful shortcut!

The line for `return self.name` is so that your snippet items will appear by name in the admin. Then under `Meta`, `verbose_name_plural` provides a plural version of the Snippet label so you can keep the grammar hawks at your workplace happy. The `unique_together` is required for `TranslatableMixin`. It ties key pieces of your models together in the database and helps keep your locales organized.

Once you've added these pieces, do your migrations steps to update the database:

```
python manage.py makemigrations
python manage.py migrate
```

## Add a template tag for the navigation menu

Now that you have a model set up, you're going to need a way to pull model data into the correct templates and locales. You're going to accomplish that with a custom [template tag](https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/). Template tags are bits of code that process data provided by a model and organize it before you pull the data into a template.

Since the template tag is related to navigation, go ahead and add a new directory to the `navigation` app called `templatetags`. In the directory, add a blank `__init__.py` file and a file called `navigation_tags.py`. Open `navigation_tags.py`. Add these three import statements to the top of the file.

```
from django import template

from wagtail.models import Page, Locale

from navigation.models import MainNavigation

register = template.Library()
```

You'll need `template` to set up the `register` variable needed for custom template tags. You'll also need the models that you're going to be manipulating, which is why you're importing `MainNavigation` and `Page` models.


 With this template tag, you're going to collect all of the items for the menu and then you're going to use a function to filter them. Open `navigation/templatetags/navigation_tags.py` and add the following code above the code for your footer template tag:

```
@register.inclusion_tag("navigation/main_navigation.html", takes_context=True)
def get_main_navigation(context):
    menu_items = []

    try:
        menu_items = MainNavigation.objects.filter(locale=Locale.get_active()).select_related("menu_page")
    except MainNavigation.DoesNotExist:
        pass

    if not menu_items:
        try:
            menu_items = MainNavigation.objects.filter(locale=Locale.get_default()).select_related("menu_page")
        except MainNavigation.DoesNotExist:
            pass
    return {
        "menu_items": menu_items,
    }
```

You could narrow down the objects to `.localized` objects in the template tag here if you wanted to rather than using `Locale`. But I want to demonstrate how you can select `.localized` objects in the template. So let's look at how to do that in the next section.

## Add a template for the navigation menu

Under `myblog/templates/navigation`, add a file called `main_navigation.html`. Then add this code to the file:

```
{% load wagtailcore_tags %}

<div class = "navigation">
    <ul>
        {% for menu_item in menu_items %}
               <li><a href = "{% pageurl menu_item.menu_page.localized %}"> {{ menu_item.name }}</a></li>
        {% endfor %}
    </ul>
</div>
```

With this code, you're using a `for` statement to sort through all of the items in the `menu_items` variable and then an `if` statement to determine which ones are `.localized` and associated with the locale of that particular page. Then you're using a default `pageurl` template tag that comes with Wagtail and the `title` for each item to create links for your navigation menu.

Now you need to add the template tag to `base.html`. Insert this code after the `<head>` section and before the `<body>` section:

```
<header>
    {% get_main_navigation %}
</header>
```

Then go up to Line 1 of `base.html` and add `main_navigation` so that the line looks like this:

```
{% load static wagtailcore_tags wagtailuserbar main_navigation %}
```

Save all of your changes if you haven't already and then run `python manage.py runserver`. You may have to restart the server to get the template tage to register properly.

Navigate to your home page at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin). Go to "Snippets" in the lefthand menu and choose "Main Navigation". Click "Add main navigation" to add a menu item. If you need some inspiration, you can name your first item "Home" with menu text "Home" and the menu URL "http://127.0.0.1:8000". You'll also want to add an item for your blog with the name "Blog", the menu text "Blog" and the URL "http://127.0.0.1:8000/blog." After adding these items, navigate to  [http://127.0.0.1:8000/en](http://127.0.0.1:8000/en) and confirm that your menu is displaying properly.

Since you've already translated your pages to French, you should see one set of pages displayed on the menu in [http://127.0.0.1:8000/en](http://127.0.0.1:8000/en) and another set displayed on [http://127.0.0.1:8000/fr](http://127.0.0.1:8000/fr).


## Add a language switcher

One last item that is super handy on a website with multiple languages is a language switcher that can rotate through the different locales.

Add a file to `myblog/templates/navigation` called `switcher.html`. Then add these lines to the file:

```
{% load i18n wagtailcore_tags %}
{% if page %}
    {% for translation in page.get_translations.live %}
        {% get_language_info for translation.locale.language_code as lang %}
        <a href="{% pageurl translation %}" rel="alternate" hreflang="{{ lang.code }}">
            {{ lang.name_local }}
        </a>
    {% endfor %}
{% endif %}
```
This code uses a combination of the i18n features in Django and Wagtail's translation features to collect all of the available live translations with `{% for translation in page.get_translations.live %}` and then collects all of the available languages with `{% get_language_info for translation.locale.language_code as lang %}`.

The next lines create a URL for each one of the translations and connects them to the appropriate language for the page that is displaying. Because there are only two locales available in this tutorial, they will just toggle back and forth between English and French.

To add the switcher to your template, got to `base.html` and update your `<header>` to look like this:

```
<header>
        {% include "navigation/switcher.html" %}
        {% get_main_navigation %}
</header>
```

# Next Steps

Now you have a working foundation for a multilingual website. You don't have _all_ the pieces though. So what could you try next? Here are some ideas:

### Add your favorite frontend

Wagtail was created to provide a backend framework that works well with as many frontend technologies as possible. Whether you prefer something simple like [Bootstrap](https://getbootstrap.com/) or something more complex like [React](https://reactjs.org/) or [Next.js](https://nextjs.org/), you can try pretty much everything with Wagtail. If you need some inspiration, Kalob Taulien did a good video on [Bootstrap](https://learnwagtail.com/tutorials/adding-bootstrap-4-theme-to-our-wagtail-website/) and Michael Yin has a good package for a [frontend setup using Webpack](https://github.com/AccordBox/python-webpack-boilerplate) that works well with Django.

### Level up your SEO

Marketing people have high expectations, and the default options in Wagtail don't typically satisfy them. So try adding one of the packages that expands your SEO options in Wagtail. The two most popular packages that are available include:

- [wagtail-metadata](https://github.com/neon-jungle/wagtail-metadata)
- [wagtail-seo](https://github.com/coderedcorp/wagtail-seo)

### Experiment with adding different elements from the Wagtail Bakery Demo

The [Wagtail Bakery Demo](https://github.com/wagtail/bakerydemo) is an example project that can provide you with some code examples to borrow for your own project. Have a look at it and see if there are any bits you like and want to try out. The navigation menu you created for this tutorial is pretty basic. The template tag created for the main navigation in the [bakery demo](https://github.com/wagtail/bakerydemo/blob/main/bakerydemo/base/templatetags/navigation_tags.py) might be one worth borrowing.

### Experiment with StreamField blocks

There is a whole list of [default blocks](https://docs.wagtail.org/en/stable/reference/streamfield/blocks.html) you can use in Wagtail. You can also combine these blocks in custom arrangements with [StructBlock](https://docs.wagtail.org/en/stable/topics/streamfield.html#structblock). If the default blocks aren't quite what you need, you can even add [custom blocks](https://docs.wagtail.org/en/stable/advanced_topics/customisation/streamfield_blocks.html#custom-streamfield-blocks) to your project. StreamField goes about as far as your imagination goes!

## Final words

Thank you for going through this tutorial with us! We hope you found it useful. If you have any questions, don't hesitate to reach out to Meagen on [Twitter](https://twitter.com/meagenvoss) or through the [Wagtail Slack Community](https://wagtail.org/slack).

## Acknowledgments

We would like to thank some folks for helping make this tutorial and workshop possible.

- **Katie McLaughlin ([@glasnt](https://github.com/glasnt))** for an amazingly thorough review and test run that caught so, so many things that could be improved. Thank you Katie!
- **Dan Bragis ([@zerolab](https://github.com/zerolab))** for taking the time to walk through Wagtail Localize questions and template questions.
- **Chris Shaw ([@chris48s](https://github.com/chris48s/))** for patiently and thoroughly answering Wagtail Localize questions.
- **Thibaud Colas ([@thibaudcolas](https://github.com/glasnt))** for spotting typos like a hawk and correcting language around Django migrations.