from django.db import models
from django.db.models import Max
from video_hosting.models import User

from django_project import settings


class Message(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    reciepient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    
    def send_message(from_user, to_user, body):
        sender_message = Message(
            user = from_user,
            sender = from_user,
            reciepient = to_user,
            body = body, 
            is_read = True)
        sender_message.save()
        
        reciepient_message = Message(
            user = to_user,
            sender = from_user,
            reciepient = from_user,
            body = body, 
            is_read = False)
        reciepient_message.save()
        return sender_message
     
    def get_message(user):
        users = []
        messages = Message.objects.filter(user=user).values("reciepient").annotate(last=Max('date')).order_by("-last")
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['reciepient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, reciepient__pk=message['reciepient'], is_read=False).count()
            })
        return users
    
    
    