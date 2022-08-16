from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model = User
    # Only display the "username"  field
    fields = ["username"]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)