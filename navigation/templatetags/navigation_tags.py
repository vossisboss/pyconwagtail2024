from django import template

from wagtail.models import Page, Locale

from navigation.models import MainNavigation

register = template.Library()


@register.inclusion_tag("navigation/main_navigation.html", takes_context=True)
def get_main_navigation(context):
    menu_items = []

    try:
        menu_items = MainNavigation.objects.filter(locale=Locale.get_active()).select_related("menu_page")
    except MainNavigation.DoesNotExist:
        pass

    if not menu_items:
        try:
            menu_items = MainNavigation.objects.filter(locale=Locale.get_default()).select_related("menu_page")
        except MainNavigation.DoesNotExist:
            pass
    return {
        "menu_items": menu_items,
    }