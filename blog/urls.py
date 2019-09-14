from django.urls import path
from .views import detail, deletePost, editPost


urlpatterns = [
    path('<int:id>', detail, name="detail"),
    path('edit/<int:id>', editPost, name="editPost"),
    path('delete/<int:id>', deletePost, name="deletePost")
]
