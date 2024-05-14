# Step Six: Using Custom Validation to Enforce Good Accessibility Practices

Let's take a look at one of the most common accessibility errors out there, but an easy one to address: **incorrect heading hierarchy**.

Taking a look at the example blog post that the management command created for you (http://127.0.0.1:8000/demo-blog-index/hello-world/), you should see we're getting an error for incorrect heading hierarchy, and it's pointing to the smaller heading in the middle of the body content. The issue here is that we have an H2 at the top of the content, but then we're skipping right to H4 on the lower heading, with no H3 between.

Screen readers and site crawlers rely on having a logical document structure to understand the content of your page, and headings are the primary way in which they interpret that structure. One way to think about this is like a big, multi-level, numbered outline in a Word document. If you indented two levels at once, that would look pretty strange and potentially confuse readers, wouldn't it? Similarly, webpage headings should avoid skipping levels, as they create the outline of the page.

Hopefully, your editors will see this warning in the accessibility checker, but you can also do more to help them avoid this mistake, using custom validation to prevent saving the page if such an error exists.

If you look at this page in the editor, you can see that the heading in question is entered into a Heading Block in the body StreamField. Wagtail 5.0, released about a year ago, introduced some [new ways to validate StreamField blocks](https://docs.wagtail.org/en/stable/releases/5.0.html#custom-validation-support-for-streamfield) (hat tip to Wagtail core developer Matt Westcott), and using these it's pretty simple to validate whether or not the headings in a StreamField are in a proper order when an editor attempts to save a page.

## Set up StreamBlock

In order to take advantage of this new functionality, we'll have to slightly adjust the structure of how we defined our StreamField. Instead of listing the possible blocks directly within the `StreamField()` declaration, we'll instead create a [Stream_Block_](https://docs.wagtail.org/en/stable/topics/streamfield.html#streamblock) class that we can apply our custom validation to.

First, create a new `blocks.py` file with the `blog` folder so we don't start to overload the `models.py` file.

Copy and paste these imports at the top of `blog/blocks.py`:

```python
from django.core.exceptions import ValidationError

from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StreamBlockValidationError,
    StructBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
```

Then cut the entire `HeadingBlock` class from `models.py` and paste it into `blocks.py`. Also remove the `blocks.` prefix that is used in three places in `HeadingBlock`, because we are now importing specific classes from the `blocks` module. The result should look like this:

```python
class HeadingBlock(StructBlock):
    size = ChoiceBlock(
        choices=[
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
    )
    text = CharBlock()

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"
```

Now we'll set up our StreamBlock. It will have all the same features of the current blog page's `body` StreamField. Copy and paste this class into your `blocks.py` file, below the `HeadingBlock`:

```python
class BaseStreamBlock(StreamBlock):
    heading = HeadingBlock()
    paragraph = RichTextBlock()
    image = ImageChooserBlock()
    embed = EmbedBlock(max_width=800, max_height=400)
```

Now, back in `models.py`, update the `body` StreamField in the `BlogPage` class to use it. Remove the list of four blocks and insert a call to the new `BaseStreamBlock`, like so:

```python
class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField(BaseStreamBlock())
```

You will also need to add an import of BaseStreamBlock to the top of `models.py`:

```python
from blog.blocks import BaseStreamBlock
```

Save everything and reload your editor. The experience should be exactly the same as it was before. You can also confirm that Django thinks nothing has changed by doing a dry run of `makemigrations`:

```shell
python manage.py makemigrations --dry-run
```


## Override `clean()` to add custom validation logic

With that rearranging done, we can now add our custom validation to check heading hierarchy on save. In a pattern that may be familiar to you if you're experienced in Django, you can override the `StreamBlock` parent class's `clean()` method that is called when saving to try to validate the StreamBlock (actually, the entire StreamField in this case). Back in `blocks.py`, we'll be updating our `BaseStreamBlock` to add the custom `clean()` method:

```python
class BaseStreamBlock(StreamBlock):
    heading = HeadingBlock()
    paragraph = RichTextBlock()
    image = ImageChooserBlock()
    embed = EmbedBlock(max_width=800, max_height=400)
    
    def clean(self, value):
        result = super().clean(value)

        headings = [
            # tuples of block index and heading level
            (0, 1)  # mock H1 block at index 0
        ]
        errors = {}

        # first iterate through all blocks in the StreamBlock
        for i in range(0, len(result)):
            # if a block is of type "heading?
            if result[i].block_type == "heading":
                # convert size string to integer
                level = int(result[i].value.get("size")[-1:])
                # append tuple of block index and heading level to list
                headings.append((i, level))

        # now iterate through list of headings,
        # starting with second heading to skip over the mock H1 heading block
        for i in range(1, len(headings)):
            # compare its level to the previous heading's level
            if int(headings[i][1]) - int(headings[i - 1][1]) > 1:
                # if the difference is more than 1,
                # add an error to the array with its original index
                errors[headings[i][0]] = ValidationError(
                    "Incorrect heading hierarchy. Avoid skipping levels."
                )

        if errors:
            raise StreamBlockValidationError(block_errors=errors)

        return result
```

This `clean()` method loops through all of the child blocks in the StreamBlock we're saving, and if they're a heading block, stores their size in a list of headings (which I prepopulated with a placeholder for the H1 that isn't part of the StreamField). Then we can loop through that list of headings – starting at the _second_ heading in the list – and compare its size to the previous heading's size. If the difference is greater than 1, we have identified an error in the heading hierarchy, so we add that to an errors dictionary, and then raise a `StreamBlockValidationError` at the end if that dictionary isn't empty.

Return to the editor after putting that in place and saving the file, and you'll see that if you try to save the "Hello, world!" blog page again, with its existing hierarchy issue, it will throw a validation error and prevent the save. Pretty cool! Swap the heading to an H2, and you'll see it save successfully. If you then add a new heading block at the bottom and set it to H4, skipping H3, you'll see that that will again throw a validation error.

You may have noticed that the accessibility checker was also flagging a heading hierarchy issue on the heading within the rich text block toward the bottom of the page. Since our rich text block is set up with the default features, editors can also create headings in rich text, in addition to the heading block. We'll need to add a little additional code to our custom `clean()` to handle headings in rich text, as they are represented differently there.

First add this new import of Python's standard regular expression library to the top of `blocks.py`:

```python
import re
```

Then add this condition below the original check to see if the block type was `heading` in the first loop through all the blocks:

```python
            elif result[i].block_type == "paragraph":
                # look for headings within the RichTextBlock and add those to the list
                for match in re.findall(r"\<h[2-6]", result[i].render()):
                    level = int(match[-1:])
                    headings.append((i, level))
```

Your whole first loop should now look like this:

```python
        # first iterate through all blocks in the StreamBlock
        for i in range(0, len(result)):
            # if a block is of type "heading?
            if result[i].block_type == "heading":
                # convert size string to integer
                level = int(result[i].value.get("size")[-1:])
                # append tuple of block index and heading level to list
                headings.append((i, level))
            elif result[i].block_type == "paragraph":
                # look for headings within the RichTextBlock and add those to the list
                for match in re.findall(r"\<h[2-6]", result[i].render()):
                    level = int(match[-1:])
                    headings.append((i, level))
```

Save the file, and if you try to save the page in the editor again, you'll now see an error being reported on the rich text block containing the H4. If a rich text block contains multiple headings, it won't be able to pinpoint an error on a specific heading, but clueing the editor into checking the whole block is still valuable.


## Further exploration

A couple of notes that we won't address in this tutorial, but would be good for you to know for the future:

- Wagtail also has `RichTextField`, a standard Django model field that can be used to provide a rich text editor outside of a StreamField. In that situation, you could subclass `RichTextField` and add your own custom `clean()` method.
- If you have a page that supports a combination of StreamField and `RichTextField`, or maybe even has other kinds of fields that result in headings on the rendered page, you can override the `clean()` method of the page model itself, looping through it all to build a complete list of headings on the page and then checking each of those in succession.


---

Our custom validation will help editors ensure they are using headings accessibly, but don't forget to make sure that any heading elements that are hardcoded into templates also follow a logical hierarchy!

[Continue to Step 7](https://github.com/vossisboss/pyconwagtail2024/tree/step-7)
