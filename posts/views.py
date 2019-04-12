from django.shortcuts import render, redirect, get_list_or_404,get_object_or_404
from .models import Post
from .form import PostForm
# Create your views here.

def list(request):
    posts = get_list_or_404(Post.objects.order_by('pk'))
    context = {'posts':posts,}
    return render(request, 'posts/list.html', context)

def create(request):                        # 글 작성을 클릭하면?
    if request.method == "POST":             # 요청이(어디서부터들어온) POST방식이면(form.html에서 정의한대로 자기 자신의링크로 POST방식으로 보내는방식)
        post_form = PostForm(request.POST, request.FILES)       # PostForm을 form 변수에 담음 , 이미지는 FILES에 있음
        if post_form.is_valid():                 # form변수(PostForm)이 유효하다면(유효성검사)
            post_form.save()                     #form을 db에 저장.
            # return render(request, 'posts/list.html') ### 왜 이건 안돼지 ?? ####
            return redirect('posts:list')   # form을 db에 저장 후 index페이지로 리다이렉트.
            
    else:
        post_form = PostForm()                   #GET방식이면(form.html이 실행되지 않으면, 즉 그냥 create를 눌렀을때.), form 변수에 담는다.
    context = {
        'post_form':post_form             #dict로 데이터를 넘김
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