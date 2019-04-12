from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.

class Post(models.Model):
    content = models.TextField()
    # image = ProcessedImageField(
    #             upload_to='posts/images',					
    #             processors=[ResizeToFill(600, 600)],		
    #             format='JPEG',								
    #             options={'quality': 90},					
    # 				)
    
    def __str__(self):
        return self.content
        
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)   # Post가 부모객체, 
    file = ProcessedImageField(
                upload_to='posts/images',					
                processors=[ResizeToFill(600, 600)],		
                format='JPEG',								
                options={'quality': 90},					
    )