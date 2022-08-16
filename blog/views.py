from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm


class PostList(generic.ListView):
    """
    This is Django's generic ListView. We are a little limited as to
    what we can do with this, but if we really needed to, we could
    access the request object here too.

    It's a class, which is why we had used class-based views in the
    original blog material. Now, to show what's going on under the
    hood, so to speak, we'll use function-based ones instead.
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


def post_detail(request, slug, *args, **kwargs):
    """
    A function-based view to view the detail of a post.
    Largely the same as the class-based, but we don't have
    different methods for GET and POST. Because it's not a
    class, all of the extra "self" stuff is removed too.

    Functionally, it's the same, but it is a bit clearer
    what's going on. To differentiate between request methods,
    we use request.method == "GET" or request.method == "POST"
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.filter(approved=True).order_by("-created_on")
    liked = False
    commented = False

    if post.likes.filter(id=request.user.id).exists():
        liked = True

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            commented = True
            comment.save()
        else:
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    return render(
        request,
        "post_detail.html",
        {
            "post": post,
            "comments": comments,
            "commented": commented,
            "liked": liked,
            "comment_form": comment_form
        },
    )


def post_like(request, slug, *args, **kwargs):
    """
    The view to update the likes. Although it should always be
    called using the POST method, we have still added some
    defensive programming to make sure.
    """
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))

def comment_delete(request, slug, id, *args, **kwargs):
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset)
    comment = post.comments.filter(id=id)
    comments = post.comments.filter(approved=True).order_by("-created_on")
    comment.delete()

    messages.add_message(request, messages.SUCCESS, 'Comment deleted!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def comment_edit(request, slug, id, *args, **kwargs):
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = post.comments.filter(id=id).first()

    comment_form = CommentForm(data=request.POST, instance=comment)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.save()
    
    messages.add_message(request, messages.SUCCESS, 'Comment Updated!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))