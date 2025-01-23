# Test Project for Django Ticket: Customizing `password_change_form` in `AdminSite`  

This project is created to demonstrate the concrete use case for making `password_change_form` in `AdminSite` customizable, as requested in [Django ticket #36121](https://code.djangoproject.com/ticket/36121).  

The project showcases how this feature would allow developers to extend the functionality of the password change process in the Django admin without duplicating the logic in the `password_change` method.

---

## Purpose  

### Current Behavior  
To customize the password change form in the Django admin, developers currently need to override the entire `password_change` method of `AdminSite`. This leads to code duplication since most of the logic in the original method must be replicated.

### Proposed Improvement  
Allowing `password_change_form` to be set as an attribute of `AdminSite`, similar to how `password_change_template` and `password_change_done_template` are handled, will enable developers to customize the form more easily and cleanly.

---

## Demonstrated Use Case  

This test project demonstrates:  

1. **Custom Validation Rules**:  
   - Prevents specific passwords, such as "forbiddenpassword," from being used.
   - Enforces secure password policies.  

2. **Additional Fields**:  
   - Adds a required "Reason for Change" field to collect a justification for why the password is being changed.  
   - Adds an "OTP" field to simulate a scenario where an admin must provide a one-time password for additional verification.  

3. **Improved Security**:  
   - Disables autocomplete for sensitive fields like `old_password`, `new_password1`, and `new_password2`.  

4. **Reduced Code Duplication**:  
   - By making `password_change_form` customizable via an attribute, this change eliminates the need to override the entire `password_change` method to implement these features.

---

## Project Features  

### Custom Authentication Form  
- **`CustomAdminAuthenticationForm`**:  
  - Disables autocomplete for the `username` and `password` fields in the admin login form.

### Custom Password Change Form  
- **`CustomAdminPasswordChangeForm`**:  
  - Adds custom fields:  
    - **Reason for Change**: Collects the reason for changing a user's password.  
    - **OTP**: Simulates an additional verification step using a one-time password.  
  - Implements custom validation to reject weak or prohibited passwords.  
  - Disables autocomplete for all password fields.  

### Custom Admin Site  
- **`CustomAdminSite`**:  
  - Demonstrates how to set `password_change_form` as an attribute to avoid duplicating logic in the `password_change` method.

---

## Code Overview  

### Custom Admin Forms (`custom_admin/forms.py`)  

```python
from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm, AdminPasswordChangeForm

class CustomAdminAuthenticationForm(AdminAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['password'].widget.attrs.update({'autocomplete': 'off'})

class CustomAdminPasswordChangeForm(AdminPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['new_password1'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['new_password2'].widget.attrs.update({'autocomplete': 'off'})

    reason_for_change = forms.CharField(
        max_length=255,
        required=True,
        label="Reason for Change",
        help_text="Provide a reason for changing this user's password."
    )
    otp = forms.CharField(
        max_length=6,
        required=True,
        label="OTP",
        help_text="Enter the code sent to your email",
    )
```

### Custom Admin (`custom_admin/views.py`)  

```python
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
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
        Handle the 'change password' task -- both form display and validation.
        """
        from django.contrib.auth.views import PasswordChangeView

        url = reverse("admin:password_change_done", current_app=self.name)
        defaults = {
            "form_class": CustomAdminPasswordChangeForm,  # Uses the custom form
            "success_url": url,
            "extra_context": {**self.each_context(request), **(extra_context or {})},
        }
        if self.password_change_template is not None:
            defaults["template_name"] = self.password_change_template
        request.current_app = self.name
        return PasswordChangeView.as_view(**defaults)(request)

custom_admin_site = CustomAdminSite(name="custom_admin")
custom_admin_site.register(User, UserAdmin)

```
## Why This Change Matters
By making password_change_form customizable via an attribute in AdminSite, developers can easily extend the password change functionality without overriding the entire method.
This aligns with the existing behavior for password_change_template and password_change_done_template, creating consistency in AdminSite.
