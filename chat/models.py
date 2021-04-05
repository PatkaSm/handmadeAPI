from django.db import models
from user.models import User


def get_or_none(class_model, **kwargs):
    try:
        return class_model.objects.get(**kwargs)
    except class_model.DoesNotExist:
        return None


class ThreadManager(models.Manager):
    def get_or_create(self, user1, user2):
        thread = get_or_none(Thread, user1=user1, user2=user2)
        if not thread:
            thread = get_or_none(Thread, user1=user2, user2=user1)
        if thread:
            return thread
        thread_obj = self.model(user1=user1, user2=user2)
        thread_obj.save()
        return thread_obj


class Thread(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user2')
    objects = ThreadManager()


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_send = models.DateTimeField(auto_now_add=True)