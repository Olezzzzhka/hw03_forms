from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.shortcuts import render, get_object_or_404, redirect

from django.conf import settings

from .models import Post, Group, User

from .forms import PostForm


def index(request):
    post_list = Post.objects.all()

    paginator = Paginator(post_list, settings.PAGINATOR_OBJECTS_PER_PAGE)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    post_list = group.posts.all()

    paginator = Paginator(post_list, settings.PAGINATOR_OBJECTS_PER_PAGE)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        "group": group,
        "page_obj": page_obj,
    }

    return render(
        request, "posts/group_list.html", context
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)

    posts = author.posts.all()

    posts_count = posts.count()

    paginator = Paginator(posts, settings.PAGINATOR_OBJECTS_PER_PAGE)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'page_obj': page_obj,
        'posts_count': posts_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author_posts_count = Post.objects.filter(author_id=post.author_id).count()
    context = {
        'post': post,
        'post_id': post_id,
        'author_posts_count': author_posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post.pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post.pk)
    context = {
        'form': form,
        'post': post,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)
