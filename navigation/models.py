from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.models import TranslatableMixin
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import PageChooserPanel


# Create your models here.
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

