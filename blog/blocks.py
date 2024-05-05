import re

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
