from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .form import PostForm, ImageForm
from .models import Post

@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)  # 권한에 ㄸㅏ라 수정삭제 버튼 없앨때 False를 추가
            post.user = request.user
            post.save()
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect('posts:list')
    else:
        post_form = PostForm()
        image_form = ImageForm()
    context = {
        'post_form': post_form,
        'image_form': image_form,
    }
    return render(request, 'posts/form.html', context)

def list(request):
    posts = Post.objects.order_by('-pk')
    context = {'posts': posts}
    return render(request, 'posts/list.html', context)

def detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    ctx = {
        'post': post,
    }
    return render(request, 'posts/detail.html', ctx)

@login_required
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    ######### 권한이 없는데 수정,삭제를 url에 입력한다면################
    if post.user != request.user:
        return redirect('posts:list')
    ######### 권한이 없는데 수정,삭제를 url에 입력한다면################
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:detail', post_pk)
    else:
        post_form = PostForm(instance=post)
    ctx = {
        'post_form': post_form,
    }
    return render(request, 'posts/form.html', ctx)

@require_POST
@login_required
def delete(request, post_pk):
    
    post = get_object_or_404(Post, pk=post_pk)
    ######### 권한이 없는데 수정,삭제를 url에 입력한다면################
    if post.user != request.user:
        return redirect('posts:list')
    ######### 권한이 없는데 수정,삭제를 url에 입력한다면################
    post.delete()
    return redirect('posts:list')
