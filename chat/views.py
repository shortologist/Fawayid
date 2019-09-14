from django.shortcuts import get_object_or_404, Http404, render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import decorators
from .models import Room, Message
from django.db.models import Q
from .forms import Message as Form
from django.http import JsonResponse


@decorators.login_required
def ChatView(request):
    user = request.user
    if user.is_authenticated:
        users = User.objects.exclude(id=user.id)
        user_paginator = Paginator(users, 5)
        query = Q(first=user) | Q(second=user)
        My_rooms = Room.objects.filter(query)
        context = {"users": user_paginator.get_page(request.GET.get("page")), "rooms": My_rooms}
        return render(request, "chat.html", context)
    raise Http404("not allowed !")


@decorators.login_required
def RoomView(request, id):
    user = request.user
    if user.is_authenticated:
        other = get_object_or_404(User, id=id)
        room = Room.objects.get_or_new(user=user, other_user=other)[0]
        paginator = Paginator(room.message_set.all()[::-1], 15)
        messages = paginator.get_page(request.GET.get("page"))[::-1]
        query = Q(first=user) | Q(second=user)
        rooms = Room.objects.filter(query)
        if request.POST:
            form = Form(request.POST)
            if form.is_valid():
                Message.objects.create(sender=user, room=room, content=form.cleaned_data["message"])
        form = Form()
        context = {"receiver": other, "sender": user, "rooms": rooms, "form": form, "messages": messages,
        "num_pages": paginator.num_pages}
        return render(request, "room.html", context)
    raise Http404("not allowed !")


def JSONChat(request, id):
    user = request.user
    if user.is_authenticated:
        other = get_object_or_404(User, id=id)
        room = Room.objects.get_or_new(user=user, other_user=other)[0]
        paginator = Paginator(room.message_set.all()[::-1], 15)
        messages = paginator.get_page(request.GET.get("page"))[::-1]
        data = []
        for message in messages:
            data.append({"message": message.content, "sender": message.sender.username, "photo_url": message.sender.profile.photo.url})
        return JsonResponse(data, safe=False)