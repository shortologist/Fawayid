from .models import Post, Comment, Viewer
from django.shortcuts import render, get_object_or_404, Http404, reverse, redirect, HttpResponseRedirect
from .forms import PostForm, CommentForm


def detail(request, id):
    post = get_object_or_404(Post, id=id)
    viewer_ip = request.META.get("REMOTE_ADDR")
    Viewer.objects.create(post=post, viewer_ip=viewer_ip)
    context = {"post": post}
    if request.user.is_authenticated:
        if request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                Comment.objects.create(writer=request.user, post=post, content=form.cleaned_data["content"])
        form = CommentForm()
        context["form"] = form
    context["comments"] = Comment.objects.filter(post=post)    
    return render(request, 'detail.html', context)


def editPost(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404("Can't do this !!")
    form = PostForm(instance=post)
    if request.POST:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('detail', args=[str(id)]))
    context = {"form": form}
    return render(request, 'edit_post.html', context)


def deletePost(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404("Can't do this !!")
    post.delete()
    return HttpResponseRedirect("/")