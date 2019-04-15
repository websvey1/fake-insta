from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):  # 이거랑, bash에서  python manage.py createsuperuser랑 뭐를 먼저 해야하나?
    list_display = ['content',]
admin.site.register(Post, PostAdmin)