from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group

from custom_admin.views import custom_admin_site

custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Group, GroupAdmin)
