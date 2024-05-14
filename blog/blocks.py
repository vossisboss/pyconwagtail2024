import re

from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StreamBlockValidationError,
    StructBlock,
    StructBlockValidationError,
    StructValue,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class HeadingBlock(StructBlock):
    size = ChoiceBlock(
        choices=[
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        help_text=mark_safe(
            "Please ensure that you do not skip heading levels. "
            "For example, the next heading after an H2 "
            "should only be either an H3 or another H2. "
            '<a href="https://www.a11yproject.com/posts/'
            'how-to-accessible-heading-structure/" target="_blank">'
            "Learn more about heading structure</a>"
        ),
    )
    text = CharBlock()

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class ImageStructValue(StructValue):
    def alt(self):
        if self.get("decorative"):
            return ""
        else:
            return self.get("alt_text") or self["image"].default_alt_text


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    alt_text = CharBlock(
        required=False,
        help_text="Use to override the image's default alt text.",
    )
    decorative = BooleanBlock(
        required=False,
        help_text="If this image does not contain meaningful content or is described in nearby text, check this box to not output its alt text.",
    )

    def clean(self, value):
        result = super().clean(value)

        if result["alt_text"] and result["decorative"]:
            raise StructBlockValidationError(
                block_errors={
                    "alt_text": ValidationError(
                        "Marking an image as decorative will override alt text entered here. Empty this field or uncheck the decorative box."
                    )
                }
            )

        phrases = (
            "graphic of",
            "image of",
            "pic of",
            "picture of",
            "photo of",
            "photograph of",
        )
        if result["alt_text"].casefold().startswith(phrases):
            raise StructBlockValidationError(
                block_errors={
                    "alt_text": ValidationError(
                        'Do not start alt text with redundant phrases like "Image of…".'
                    )
                }
            )

        return result

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"
        value_class = ImageStructValue


class BaseStreamBlock(StreamBlock):
    heading = HeadingBlock()
    paragraph = RichTextBlock()
    image = ImageBlock()
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
            elif result[i].block_type == "paragraph":
                # look for headings within the RichTextBlock and add those to the list
                for match in re.findall(r"\<h[2-6]", result[i].render()):
                    level = int(match[-1:])
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
