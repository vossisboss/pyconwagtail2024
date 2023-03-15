# Step Five: Add translatable navigation

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