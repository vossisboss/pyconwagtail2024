from django.db import models

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, HelpPanel, InlinePanel
from wagtail.search import index

from modelcluster.fields import ParentalKey

from blog.blocks import BaseStreamBlock


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    subpage_types = ['blog.BlogPage']


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField(BaseStreamBlock())

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    parent_page_types = ['blog.BlogIndexPage']


class ImageGalleryPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        HelpPanel(
            content=(
                "<hr>"
                "<p>The <b>alt text</b> field is for entering a text alternative "
                "to be displayed if images fail to load, "
                "or to be read by screen reader software. "
                "If one is not entered below, the image's default alt text will be used.</p>"
                '<a href="https://www.a11yproject.com/posts/alt-text/" '
                'target="_blank">Learn more about writing good alt text</a>'
            )
        ),
        InlinePanel("gallery_images", label="Images"),
    ]


class ImageGalleryImageImage(Orderable):
    page = ParentalKey(
        ImageGalleryPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "custom_media.CustomImage", on_delete=models.CASCADE, related_name="+"
    )
    alt_text = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel("image"),
        FieldPanel("alt_text"),
    ]
