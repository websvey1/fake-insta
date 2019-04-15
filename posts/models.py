from django.db import models    # 장고모델 임포트
from django.conf import settings # 모델에 user를 추가하며 생긴 settings
from imagekit.models import ProcessedImageField #이미지 업로드
from imagekit.processors import ResizeToFill #이미지 수정

# Create your models here.

class Post(models.Model): # Post라는 모델을 생성
    content = models.TextField() 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 권한설정을 위한 외래키,
    def __str__(self):
        return self.content
        
class Image(models.Model):       #사진올리기위해 이미지 모델을 만든다
    post = models.ForeignKey(Post, on_delete=models.CASCADE)   # Post가 부모객체, 
    file = ProcessedImageField(
                blank=True,    # 빈값도 가능함,
                upload_to='posts/images',	 #이미지를 업로드하면 해당ㄹ경로로
                processors=[ResizeToFill(600, 600)],		#자르기
                format='JPEG',								#포맷
                options={'quality': 90},					#퀄리디설정
    )
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 우리가 만든게 아니라 정해진 단어를 써야함
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 우리가 만든 모델이라서 Post만 쓰면 된다
    content = models.CharField(max_length=140)
    
    def __str__(self):
        return self.content