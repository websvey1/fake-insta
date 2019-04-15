from django import forms
from .models import Post, Image

class PostForm(forms.ModelForm):           # forms.py의 역할 ? - 모델에서 정의한 컬럼 중 필요한 것만 사용하려고?
    class Meta:                                                # 이미지 중복 선택과 같은 세세한 설정을 하려고?
        model = Post
        fields = ['content',]

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file',]
        widgets = {
            'file':forms.FileInput(attrs={'multiple':True}), #  이미지 중복선택이 가능하다. 이건 모델에서 불가능한지?
        }
        