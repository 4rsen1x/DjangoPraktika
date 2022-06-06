from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.views import generic
from .forms import CommentForm, PostForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'

def redirect_from_blog(request):
    response = redirect('/')
    return response

def post_detail(request, slug):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def add_post(request):
    template_name = 'blog/add_post.html'
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit = False)
            new_post.author = request.user
            new_post.save()
            respone = redirect('/')
            return respone
    else:
        post_form = PostForm()

    return render(request, template_name, {'post_form': post_form})