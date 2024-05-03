from wagtail import hooks
from wagtail.admin.userbar import AccessibilityItem


class CustomAccessibilityItem(AccessibilityItem):
    def get_axe_run_only(self, request):
        # Do not limit what rule sets run if the user is a superuser
        if request.user.is_superuser:
            return None
        # Otherwise, use the default rule sets
        return AccessibilityItem.axe_run_only


@hooks.register("construct_wagtail_userbar")
def replace_userbar_accessibility_item(request, items):
    items[:] = [
        CustomAccessibilityItem() if isinstance(item, AccessibilityItem) else item
        for item in items
    ]
