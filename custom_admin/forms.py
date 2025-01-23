from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm, AdminPasswordChangeForm


class CustomAdminAuthenticationForm(AdminAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable autocomplete for username and password fields
        self.fields['username'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['password'].widget.attrs.update({'autocomplete': 'off'})


class CustomAdminPasswordChangeForm(AdminPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable autocomplete for all fields for security reasons
        self.fields['old_password'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['new_password1'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['new_password2'].widget.attrs.update({'autocomplete': 'off'})

    # To add more fields, examples:
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

    def clean_new_password2(self):
        password = self.cleaned_data.get('new_password2')
        if password == "forbiddenpassword":
            raise forms.ValidationError("You cannot use 'forbiddenpassword' as your password.")
        return password
