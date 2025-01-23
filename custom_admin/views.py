from django.contrib.admin import AdminSite
from django.urls import reverse

from custom_admin.forms import CustomAdminAuthenticationForm, CustomAdminPasswordChangeForm


class CustomAdminSite(AdminSite):
    login_form = CustomAdminAuthenticationForm

    # Suggested Solution
    # ----------------------
    password_change_form = CustomAdminPasswordChangeForm

    # Current Solution
    # ----------------------
    # In order to apply this customization I should override whole the method and duplicate its codes.
    # But we can set it as an attribute to prevent this code duplicating.
    def password_change(self, request, extra_context=None):
        """
        Handle the "change password" task -- both form display and validation.
        """
        from django.contrib.auth.views import PasswordChangeView

        url = reverse("admin:password_change_done", current_app=self.name)
        defaults = {
            "form_class": CustomAdminPasswordChangeForm,
            "success_url": url,
            "extra_context": {**self.each_context(request), **(extra_context or {})},
        }
        if self.password_change_template is not None:
            defaults["template_name"] = self.password_change_template
        request.current_app = self.name
        return PasswordChangeView.as_view(**defaults)(request)

custom_admin_site = CustomAdminSite(name="custom_admin")

