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

Now save your code and run the migration commands `python manage.py makemigrations` and `python manage.py migrate`.

## :warning: Note :warning:

If you get an error message related to database fields at this point, then you'll have to remove the database. To do that, delete the `db.sqlite3` file. Then run the `makemigrations` and `migrate` commands again to reapply the migration files to the database. 

Since you deleted the database, you're going to have to create a new superuser to access the admin section of Wagtail again. So run `python manage.py createsuperuser` to create a new superuser. Then test it by running `python manage.py runserver` and navigating to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to log in.

Now you have a good foundation for customizing your `Image` model. You might not feel like this has added a lot to the project so far. But it's wayyyyy better to update these models when you don't have a lot of data to work with. Next, we're going to add some additional models to our code and start building out a blog.