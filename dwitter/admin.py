from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from .models import Dweet
from .models import Profile

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    # Only display the "username"  field
    fields = ["username"]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Dweet)
# Removing the register Profile site
# admin.site.register(Profile)