# Step Three: Add custom models

One thing we always like to call attention to is custom models. Because Wagtail is built on top of Django, it has the same quirks as Django does when it comes to custom models. In the [Django documentation on customizing authentication](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project), it says "It’s highly recommended to set up a custom user model, even if the default User model is sufficient for you." This is because creating a custom user model in the middle of a project or with an existing database is a huge hassle. Even very smart people haven't figure out how to create a migration fix for it yet. The ticket to solve this issue has been open for _years_.

Anyway, we're bringing this up because Wagtail has some other models that are worth customizing before you go too far into a project so that you can save yourself some grief later on. For this workshop, we're only going to work with the `Image` and `Renditions` models today, but we'll provide reference links for the other Wagtail models you should customize, including the `User` model and the Wagtail `Documents` model.

No matter what model you customize, you should be aware that transitioning data to a new model can be somewhat tricky. The more work you do to set up these models well before any data is added to the database, the better.

Now, most of the work has already been done for you in the project template to save us a bit of time, but we're going to walk through the model so that you know what it is and why it's important.

Because we're using the separate app structure for our project, our custom model is in the `custom_media` app. Open the `custom_media` folder and go to `models.py`. Let's have a look at the code in the file:

```python
from django.db import models

from wagtail.images.models import Image, AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    # Add any extra fields to image here

    # To add a caption field:
    # caption = models.CharField(max_length=255, blank=True)
    default_alt_text = models.CharField(max_length=255, blank=False)

    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        "default_alt_text",
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
```

The default Wagtail image model DOES NOT include designated fields for alt text or for image captions. By default, Wagtail will take the title of any image that is used and use that title as the alt text on a webpage.

As we will get into in more detail later, this is NOT ideal. Alt text is very important for people who navigate websites with screenreaders, but context matters a lot. Sometimes, the title for an image works perfectly well. But if the image is decorative (like a logo), then it can be really annoying for a screenreader user to navigate through a bunch of titles that don't provide good information for them. The current default does provide the most flexibility for developers to customize projects according to their specific needs and accessibility standards, though.

Still, it is a very good idea to have a standard `default_alt_text` field, which is why one has been added to our `CustomImage` model. We also added `blank=False` to make it a mandatory field so that people won't forget to add it.

We'll include some instructions on how to add the custom model at the end, just in case you ever have to set this up from scratch. Next, we're going to start building out a blog.


---

[Continue to step 4](https://github.com/vossisboss/pyconwagtail2024/tree/step-4)
