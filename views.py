from django.shortcuts import render, HttpResponseRedirect
from django.core.paginator import Paginator
from .blog.models import Post
from .content.models import SocialLink, About, Header
from .category.models import Category
from .blog.forms import PostForm


def home(request):
    queryset = Post.objects.all()
    paginator = Paginator(queryset, 2)
    pageNum = request.GET.get("page")
    page = paginator.get_page(pageNum)
    socialLinks = SocialLink.objects.filter(active=True)
    about = About.objects.get(active=True)
    header = Header.objects.get(active=True)
    form = PostForm()
    if request.POST:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=True)
            post.author = request.user
            post.save()
            return HttpResponseRedirect("/")
    context = {"page": page, "links": socialLinks, "about": about,
               "header": header, "form": form, "social": socialLinks}
    return render(request, "home.html", context)
