from django.urls import path
from .views import CategoryView

urlpatterns = [
    path('<int:id>', CategoryView, name='category')
]