from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from carbon_usage.models import User

# from django.contrib.auth import get_user_model
# User = get_user_model()


admin.site.register(User, DjangoUserAdmin)
