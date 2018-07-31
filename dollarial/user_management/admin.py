from django.contrib import admin

from user_management.models import User, Clerk


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Clerk)
class ClerkAdmin(admin.ModelAdmin):
    pass
