from django.shortcuts import render, redirect, get_list_or_404,get_object_or_404
from .models import Post, Image
from .form import PostForm, ImageForm
# Create your views here.

def list(request):
    posts = get_list_or_404(Post.objects.order_by('pk'))
    context = {'posts':posts,}
    return render(request, 'posts/list.html', context)

def create(request):                        # 글 작성을 클릭하면?
    if request.method == "POST":             # 요청이(어디서부터들어온) POST방식이면(form.html에서 정의한대로 자기 자신의링크로 POST방식으로 보내는방식)
        post_form = PostForm(request.POST)       # PostForm을 form 변수에 담음 , 이미지는 FILES에 있음 , 이미지 따로 넣을거니까 부분을 뺀다
        if post_form.is_valid():                 # form변수(PostForm)이 유효하다면(유효성검사)
            post = post_form.save()                     #form을 db에 저장. # 게시글은 여기서 끝 !!!!##############
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            # return render(request, 'posts/list.html') ### 왜 이건 안돼지 ?? ####
            return redirect('posts:list')   # form을 db에 저장 후 index페이지로 리다이렉트.
            
    else:
        post_form = PostForm()                   #GET방식이면(form.html이 실행되지 않으면, 즉 그냥 create를 눌렀을때.), form 변수에 담는다.
        image_form = ImageForm()
    context = {
        'post_form':post_form,             #dict로 데이터를 넘김
        'image_form':image_form
    }
    return render(request, 'posts/form.html', context)   # 생성폼을 실행.

def update(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    else:
        post_form = PostForm(instance=post)
    context = {
        'post_form':post_form
    }
    return render(request, 'posts/form.html', context)

def delete(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    if request.method == "POST":
        post.delete()
    return redirect('posts:list')