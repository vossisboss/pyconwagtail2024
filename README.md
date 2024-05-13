# Step Two: Extend home page model

Before you start adding content, you'll need to add some models to Wagtail. Wagtail models are derived from [Django models](https://docs.djangoproject.com/en/4.1/topics/db/models/). One key difference in writing models for Wagtail is that adding views isn't necessary unless you need to create a highly customized view or form. We'll go over this in a bit more detail when you add templates to your project. For right now, you mostly need to know that models provide the essential fields and structures for the content on your Wagtail site that will be stored in your database.

Many of the steps you'll be doing here have been borrowed from the [Getting Started tutorial](https://docs.wagtail.org/en/stable/getting_started/tutorial.html) for Wagtail.

## Extending the `HomePage` model

Right out of the box, Wagtail comes with a `home` app that provides a blank `HomePage` model. This model will define the home page of your website and what content appears on it. Go to the `home` directory in your project and open up `models.py`. You'll see that all the model currently has in it by default is a `pass` command. So you're going to have to extend it to add content to your home page.

Since this is going to be a blog site, you should probably tell your readers what the blog is about and give them a reason to read it. All pages in Wagtail have a title by default, so you'll be able to add the blog title easily. So let's extend the `HomePage` model by adding a text field for a blog summary to the model.

First, you'll need to add some additional import statements to the top of the page. This statement will import the `RichTextField` (one that lets you use bold, italics, and other formatting) from Wagtail:

```python
from wagtail.fields import RichTextField
```

And this statement will import the panel you need to make sure your new field appears in the Wagtail admin as well:

```python
from wagtail.admin.panels import FieldPanel
```

Once those import statements are added, delete `pass` from your `HomePage` model and replace it with:

```python
    summary = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
    ]
```

Your whole file should look like this right now:

```python
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

```python
    main_image = models.ForeignKey(
        images.get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
```

Then we need one more imput for the images module:

```python
from wagtail import images
```

And then add another line to `content_panels`:

```python
        FieldPanel('main_image'),
```

Your full `models.py` file should like like this now:

```python
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail import images


class HomePage(Page):
    summary = RichTextField(blank=True)
    main_image = models.ForeignKey(
        images.get_image_model_string(),
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

```shell
python manage.py makemigrations
python manage.py migrate
```

## Check your fields with the development server 

If it's not still going, let's get the development server up and running in your terminal with:

```shell
python manage.py runserver
```

Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to check that your homepage is still functional. Then navigate to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to access the admin log in page. Log in with the superuser you created in Step One.

Now you're in the Wagtail dashboard. You'll see lots of handy stuff like a list of the number of pages, your latest revisions, and other useful things. On the left hand side is the main toolbar for Wagtail. Select "Pages" from this toolbar and then click the "Home" link.

You'll be taken to the Home parent page listing, which is pretty empty right now because there aren't any pages inheriting from the Home page yet. Click the three little dots next to "Home" at the top of the page to open the action menu. Choose "Edit".

Now we're going to add some data to our blog. Feel free to choose your own theme. But if you're not feeling particularly inspired, you can join me in filling out "Badger Bonanza" for the title and "Musings on Earth's most noble and distinctive mammal" for the summary. You'll need a picture too. Feel free to use this [lovely badger](https://upload.wikimedia.org/wikipedia/commons/4/41/M%C3%A4yr%C3%A4_%C3%84ht%C3%A4ri_4.jpg) from Wikimedia Commons. Click "Choose an image" and then upload the image to Wagtail.

![Screenshot of home page in Wagtail admin](https://www.meagenvoss.com/media/images/Screen_Shot_2022-09-28_at_9.16.11_PM.original.png)

When you're done adding the content, go to the bottom of the page and use the big green button to save your draft. Then click on the arrow next to "Save draft" to open up the publish menu and click "Publish" to publish the page.

![Screenshot of Wagtail publish button](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-05_at_11.56.07_PM.original.png)

Go ahead and click the "View Live" link when it comes up.

Oh no! There's no badger! Did we do something wrong? Nope. We have to remove the default homepage that came with Wagtail, so let's do that.

## Remove the default homepage

Go to `home/templates/home/home_page.html` and delete everything in the file except for the first line `{% extends "base.html" %}`. Update the file so it looks like this:

```django
{% extends "base.html" %}
{% load wagtailcore_tags wagtailimages_tags %}

{% block body_class %}template-homepage{% endblock %}

{% block content %}

<h1>{{ page.title }}</h1>

<div>{{ page.summary }}</div>

{% image page.main_image max-500x500 %}

{% endblock %}
```

Save the file and then reload your homepage. You should now see the title of your blog, the summary, and a beautiful badger (if you chose to go with my badger theme rather than your own).

Now, the summary might look a little funky. And that is because text fields do not print with escaped characters by default. Fortunately, Wagtail comes with a handy filter, among many other [handy filters](https://docs.wagtail.org/en/stable/topics/writing_templates.html#template-tags-and-filters), that can render the text properly. Update the `{{ page.summary }}` line so that it is:

```django
<div>{{ page.summary|richtext }}</div>
```

Refresh the page and the summary text should be displaying properly now.

Before you move on from this task, let's clean your templates and organize things a bit. Navigate to `myblog/templates` and create a new directory in it called `home`. Move `home_page.html` to the new `home` directory. Refresh the page to make sure it still works. The delete the `templates` directory in the `home` app. While you're there, you can also delete the `static` folder in the the `home` app because all that is in it is some CSS for the default home page.

This structure will help you stay organized by keeping all of your templates in one directory. Trust me, any frontend developers you work with will thank you. And then they will find something else to pick on, but that's the way of things.
