from django.urls import path
from .views import ChatView, RoomView, JSONChat

urlpatterns = [
    path('', ChatView, name="chat"),
    path('<int:id>', RoomView, name="room"),
    path('json/<int:id>', JSONChat)
]