from django import template

from wagtail.models import Page

from navigation.models import MainNavigation

register = template.Library()

def filter_nav_for_locale(cls, locale):
    menu_items = None

    try:
        menu_items = cls.objects.filter(locale=locale)
    except cls.DoesNotExist:
        pass

    if not menu_items:
        try:
            menu_items = cls.objects.filter(locale=default_language())
        except cls.DoesNotExist:
            pass

    return menu_items

@register.inclusion_tag("navigation/main_navigation.html", takes_context=True)
def get_main_navigation(context):
    menu_items = []
    if MainNavigation.objects.all() is not None:
        menu_page_id = MainNavigation.objects.values('menu_page_id')
        menu_items = Page.objects.live().filter(id__in=menu_page_id)
    return {
        "menu_items": menu_items,
    }