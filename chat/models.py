from django.db import models
from django.contrib.auth.models import User


class RoomManager(models.Manager):

    def get_or_new(self, user, other_user):
        username = user.username
        other_user = other_user.username
        if username == other_user:
            return None, False
        q1 = models.Q(first__username=username) & models.Q(second__username=other_user)
        q2 = models.Q(second__username=username) & models.Q(first__username=other_user)
        qs = self.get_queryset().filter(q1 | q2)
        if qs.count() == 1:
            return qs.first(), False
        else:
            other = User.objects.get(username=other_user)
            obj = self.model(
                first=user,
                second=other
            )
            obj.save()
            return obj, True


class Room(models.Model):
    first = models.ForeignKey(User, on_delete=models.CASCADE, related_name="first_user")
    second = models.ForeignKey(User, on_delete=models.CASCADE, related_name="second_user")
    slug = models.SlugField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    start = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    objects = RoomManager()

    def __str__(self):
        return str(self.second)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_seender")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content
