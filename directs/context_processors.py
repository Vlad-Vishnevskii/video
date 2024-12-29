from directs.models import Message
from video_hosting.models import MeetingRequest

def has_unread_notifications(request):
    if request.user.is_authenticated:
        # Проверяем наличие хотя бы одного непрочитанного сообщения
        has_unread_messages = Message.objects.filter(user=request.user, is_read=False).exists()
        has_unread_requests =  MeetingRequest.objects.filter(to_user=request.user, status="send").exists()
        has_unread = has_unread_messages or has_unread_requests 
    else:
        has_unread = False
    return {'has_unread_notifications': has_unread}