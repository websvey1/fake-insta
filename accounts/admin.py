from django.contrib import admin

# Register your models here.
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'nickname', 'introduction', 'user_id',
    ]
admin.site.register(Profile, ProfileAdmin)