from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Category
from .forms import PostCategoryForm


def CategoryView(request, id):
    category = get_object_or_404(Category, id=id)
    queryset = category.post_set.all()
    print(queryset)
    paginator = Paginator(queryset, 2)
    pageNum = request.GET.get("page")
    page = paginator.get_page(pageNum)
    form = PostCategoryForm()
    if request.user.is_authenticated and request.POST:
        form = PostCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=True)
            post.category = category
            post.author = request.user
            post.save()
            return redirect("category", id=5)
    return render(request, "category.html", {"category": category, "page": page, "form": form})
