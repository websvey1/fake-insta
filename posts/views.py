from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain
from .form import PostForm, ImageForm, CommentForm
from .models import Post, Comment, Image, Hashtag

@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)  # 권한에 ㄸㅏ라 수정삭제 버튼 없앨때 False를 추가
            post.user = request.user
            post.save()
            # hashtag - post.save()가 된 이후에 해시태그 코드가 와야함.
            # 1 게시글을 순회하면서 띄어쓰기를 잘라야 함
            for word in post.content.split():
                # 2 자른 단어가 #으로 시작하는지를 파악해야함
                if word[0] =='#':
                # if word.startswith('#'): #이것도 같다
                    hashtag = Hashtag.objects.get_or_create(content=word) 
                    #Hashtag(모델객체)의 인스턴스와 boolean을 return
                    # 3 이 해시태그가 기존 해시태그에 있는건지?
                    post.hashtags.add(hashtag[0])
            
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
    ########### 1 #############
    followings=request.user.followings.all()
    posts = Post.objects.filter(Q(user__in=followings) | Q(user=request.user.id)).order_by('-pk')
    
    ############# 2 ###########
    # followings = request.user.followings.all()
    # chain_followings = chain(followings, [request.user])
    
    # posts = Post.objects.filter(user__in=chain_followings).order_by('-pk')
    # posts = Post.objects.filter(user__in=request.user.followings.all()).order_by('-pk')
    comment_form = CommentForm()         #댓글 작성하기 위한 form 정의를 해야 인덱스에서 폼이 보임
    context = {'posts': posts,
        'form':comment_form
    }
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
            post = post_form.save()
            #hash tag update
            # 1 게시글을 순회하면서 띄어쓰기를 잘라야 함
            post.hashtags.clear()
            for word in post.content.split():
                if word[0] =='#':
                    hashtag = Hashtag.objects.get_or_create(content=word) 
                    #Hashtag(모델객체)의 인스턴스와 boolean을 return
                    # 3 이 해시태그가 기존 해시태그에 있는건지?
                    post.hashtags.add(hashtag[0])
            return redirect('posts:list')
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

@require_POST
@login_required
def comments_create(request, post_pk): # 여기 post는 어디서 오는걸까
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user # 객체를 가져옴
        comment.post_id = post_pk # 객체로 가져오면 커리문이 한번 더 돌기때문에 바로 키를 가져옴?
        comment.save()
    return redirect('posts:list')

@require_POST
@login_required
def comments_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()    
    return redirect(f'/posts/#{post_pk}')

@login_required
def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    ####### 1번 방법 ################
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('posts:list')
    ##### 2번방법#####################
    # user = request.user
    # if post.like_users.filter(pk=user.pk).exists():
    #     post.like_users.remove()

def explore(request):
    posts = Post.objects.order_by('-pk')
    # posts = Post.objects.exclude(user=request.user).order_by('-pk')
    
    comment_form = CommentForm()
    context = {
        'posts':posts,
        'form':comment_form,
    }
    return render(request, 'posts/explore.html', context)

def hashtag(request, hash_pk):
    hashtag = get_object_or_404(Hashtag, pk=hash_pk)
    posts = hashtag.post_set.order_by('-pk')
    context = {
        'hashtag':hashtag,
        'posts':posts,
    }
    return render(request, 'posts/hashtag.html', context)