from django.contrib import admin
from .models import Profile, User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'nickname', 'introduction', 'user_id',
    ]
admin.site.register(Profile, ProfileAdmin)

admin.site.register(User, UserAdmin)