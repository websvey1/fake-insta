from django.contrib import admin
from .models import Post,Image,Hashtag
# Register your models here.

class PostAdmin(admin.ModelAdmin):  # 이거랑, bash에서  python manage.py createsuperuser랑 뭐를 먼저 해야하나?
    list_display = ['content',]
admin.site.register(Post, PostAdmin)

class ImageAdmin(admin.ModelAdmin):  # 이거랑, bash에서  python manage.py createsuperuser랑 뭐를 먼저 해야하나?
    list_display = ['file','post_id',]
admin.site.register(Image, ImageAdmin)

class HashtagAdmin(admin.ModelAdmin):
    list_display = ['content']
admin.site.register(Hashtag, HashtagAdmin)