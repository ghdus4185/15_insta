from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from .models import HashTag, Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)

    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context)


@login_required
def create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            for word in post.content.split():
                if word.startswith('#'):
                    # 해쉬태그 추가
                    hashtag = HashTag.objects.get_or_create(
                        content=word)[0]  # (object, True or False)
                    post.hashtags.add(hashtag)
            return redirect("posts:index")
    else:
        form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/form.html', context)


def update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            post.hashtags.clear()
            for word in post.content.split():
                if word.startswith('#'):
                    # 해쉬태그 추가
                    hashtag = HashTag.objects.get_or_create(
                        content=word)[0]  # (object, True or False)
                    post.hashtags.add(hashtag)
            return redirect("posts:index")
    else:
        form = PostForm(instance=post)
    context = {
        'form': form
    }
    return render(request, 'posts/form.html', context)


def hashtags(request, id):
    hashtag = get_object_or_404(HashTag, id=id)
    posts = hashtag.taged_posts.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context)


@login_required
def like(request, id):
    post = get_object_or_404(Post, id=id)
    user = request.user
    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
    return redirect('posts:index')


@login_required
def delete(request, id):
    post = get_object_or_404(Post, id=id)
    if post.user == request.user:
        post.delete()
    return redirect('posts:index')


def detail(request, id):
    post = get_object_or_404(Post, id=id)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form
    }
    return render(request, 'posts/detail.html', context)


def comment_create(request, id):
    post = get_object_or_404(Post, id=id)
    comments_form = CommentForm(request.POST)
    if comments_form.is_valid():
        comment_ = comments_form.save(commit=False)
        comment_.post = post
        comment_.user = request.user
        comment_.save()
    return redirect('posts:detail', id)
