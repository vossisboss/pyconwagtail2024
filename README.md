# Step Three: Add custom models

One thing I always like to call attention to is custom models. Because Wagtail is built on top of Django, it has the same quirks as Django does when it comes to custom models. In the Django documentation, it says "It’s highly recommended to set up a custom user model, even if the default User model is sufficient for you." This is because creating a custom user model in the middle of a project or with an existing database is a huge hassle. Even very smart people haven't figure out how to create a migration fix for it yet. The ticket to solve this issue has been open for _years_.

Anyway, I bring this up because Wagtail has some other models that are worth customizing before you go too far into a project so that you can save yourself some grief later on. For this workshop, we're only going to set up the custom `Image` and `Renditions` models today, but we'll provide reference links for the other Wagtail models you should customize, including the `User` model and the Wagtail `Documents` model.

Because we're using the separate app structure for our project, we're going to put our custom models in a `custom_media` app. Type the following command into your terminal:

```
python manage.py startapp custom_media
```

Then update the code in your `INSTALLED_APPS` in `myblog/settings/base.py` to include the new apps:

```
INSTALLED_APPS = [
    "home",
    "search",
    "custom_media",
]

```


Now let's navigate to `custom_media/models.py` and update the file so that it looks like this:

```
from django.db import models
from wagtail.documents.models import Document, AbstractDocument

from wagtail.images.models import Image, AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    # Add any extra fields to image here

    # To add a caption field:
    # caption = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        # 'caption',
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
```

Let's take a closer look at some of the comments in the code here. You'll notice that there is an option to add a `caption` field to the image model. Wagtail doesn't include an image caption by default. Many projects need an image caption field for crediting photographers and artists. The `CustomImage` model is the best place to do that.

The `CustomImage` model is also one of the best places to add a field for alt text, which is very important for people who navigate websites with screenreaders. By default, Wagtail uses the title of an image for the alt text. This is not ideal, but currently that default provides the most flexibility for developers to customize projects according to their specific needs and accessibility standards.

Still, it is a good idea to add a standard `default_alt_text` field, so we're going to go ahead and add one to our `CustomImage` model and make it mandatory so that people won't forget to add it.

Add the following line under the comment line for the caption field:

```
default_alt_text = models.CharField(max_length=255, blank=True)
```

So now the full `models.py` file should look like:

```
from django.db import models
from wagtail.documents.models import Document, AbstractDocument

from wagtail.images.models import Image, AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    # Add any extra fields to image here

    # To add a caption field:
    # caption = models.CharField(max_length=255, blank=True)
    default_alt_text = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        # 'caption',
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
```

Once you have the models set up, you'll have to updating your image model reference. First, you'll need to add the following settings to the bottom of your `base.py` settings file:

```
# Custom models

WAGTAILIMAGES_IMAGE_MODEL = 'custom_media.CustomImage'

```


Thie setting tells Wagtail which custom model you're using. Even with this set though, you're going to have update some references in your code as well. Fortunately, you only need to make one update for this particular project. Navigate to `home/models.py`. Then add the following import statement to the top of your file:

```
from wagtail import images
```
Then update your `main_image` model so that it looks like this:

```
    main_image = models.ForeignKey(
        images.get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
```
What you're doing with this code is collecting the string for the name of your CustomImage model so that you can point Wagtail to your custom model instead of the default `wagtailimages` model.

### Custom User model

Now, you might be wondering why I didn't have you go through the migration steps after adding those last few models. Welp, it's because we've been reaching the part of the tutorial I've been warning you about. After we add the `CustomUser` model, we're going to have to reset our migrations. Why? Let's find out together here.

First, navigate to `custom_user/models.py` and add the following code to your file and save it:

```
from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
```
Then navigate to your `base.py` file in settings and update the `Custom model` section to include the custom user model:

```
# Custom models

WAGTAILIMAGES_IMAGE_MODEL = 'custom_media.CustomImage'

WAGTAILDOCS_DOCUMENT_MODEL = 'custom_media.CustomDocument'

AUTH_USER_MODEL = 'custom_user.User'
```


Now save your code and run the migration commands `python manage.py makemigrations` and `python manage.py migrate`. You should get an error message that is similar to "Migration admin.0001_initial is applied before its dependency app.0001_initial on database 'default' ". Tables related to the `User` model in Django are some of the very first that are set up when you start a new project. So if you try to apply a custom version of the `User` model after the initial migration for your first app, you're going to get an error.

How do we fix this then? There are a few different appraoches you can take. Because your project is still in development though and you're currently using the default sqlite database for working on it, one of the easiest approaches for beginners to learn is to reset the migrations.

There are multiple approaches to resetting migrations too. But for this project, we're going to delete all our existing migration files along with the database then run our migration commands again. Here's how you do that.

1. Go to each `migrations` folder for the `blog` app (we'll go in alaphabetical order).
2. Delete all of the files in the folder except for `__init.py__`.
3. Open the `pycache` folder in the `migrations` folder and delete all of the files there as well.

Repeat this process for the `home` app. There shouldn't be any migration files in `custom_media` or `custom_user` yet but you can doublecheck that if you want. Next, find your database. It should have a name like `db.sqlite3`. Delete your database file as well.

Make sure one more time that all of your migration files have been removed. Then run your first migration command `python manage.py makemigrations` to create the new migrations you need. If you receive an error, delete all of the migration files and the database again. Be extra sure the you removed the `pycache` files in each app as well. If there is no error, then run `python manage.py migrate` to create fresh migrations in your database.

Since you deleted the database, you're going to have to create a new superuser to access the admin section of Wagtail again. So run `python manage.py createsuperuser` to create a new superuser. Then test it by running `python manage.py runserver` and navigating to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to log in.

Now you have a good foundation for customizing these critical models. You might not feel like this has added a lot to the project. But trust me, you'll be glad you took these steps further down the line. Next, we're going to add some additional models to our code called `snippets` along with some templates that will help our website look a little nicer.