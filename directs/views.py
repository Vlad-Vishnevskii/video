from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from directs.models import Message
from video_hosting.models import User, MeetingRequest
from django.core.paginator import Paginator
from django.db.models import Q
import random

@login_required
def inbox(request):
    user = request.user
    use = list(User.objects.all())
    for d in use:
        if d == user:
            use.remove(d)
        else:
            pass
    print(use)
    #if len(random_items) > 1:
    users = random.sample(use, 1)
    users1 = random.sample(use, 1)
    print(users)
    messages = Message.get_message(user=request.user)
    other_pep = User.objects.all()
    active_direct = None
    directs = None
    paginator = Paginator(users, 8)
    page_number = request.GET.get('page')
    users_paginator = paginator.get_page(page_number)
    paginator1 = Paginator(users1, 8)
    page_number1 = request.GET.get('page')
    users_paginator1 = paginator1.get_page(page_number1)
    incomingMeet = MeetingRequest.objects.filter(to_user=user, status="send").order_by("-created_at").first()   
    to = request.path
    to = to.split('/')[-1]
    print(messages)
    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(
            Q(sender=user) | Q(reciepient=user)
        ).order_by('-date')  # Сортируем по дате в обратном порядке

        # Создаем словарь для хранения чатов
        chats = {}

        for message in directs:
            other_user = message.reciepient if message.sender == user else message.sender
            if str(other_user) != str(request.user):
                if other_user not in chats:
                    print(other_user.avatar)
                    chats[other_user] = []
                chats[other_user].append(message)


        print(chats)
        context = {
            'users': users,
            'users1': users1,
            'chats': chats,
            'active_direct': active_direct,
            'messages': messages,
            'other_pep': other_pep,
            'request': request,
            'users': users_paginator,
            'users1': users_paginator1,
            'incomingMeet': incomingMeet,
        }

        return render(request, 'directs/test_inbox.html', context)
    else:
        context = {
            'users': users,
            'users1': users1,
            'chats': None,
            'active_direct': None,
            'messages': None,
            'other_pep': other_pep,
            'request': request,
            'users': users_paginator,
            'users1': users_paginator1,
            'incomingMeet': incomingMeet,
        }
        return render(request, 'directs/test_inbox.html', context)

def Directs(request, username):
    user = request.user
    messages = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, reciepient__username=username)
    directs.update(is_read=True)
    to = request.path
    
    

    to = to.split('/')[-1]
    meet = MeetingRequest.objects.filter(from_user=user).values("to_user").order_by("-created_at")
    Message.objects.filter(user=user, is_read=False).update(is_read=True)
    
    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0
            
    context = {
            'meet': meet,
            'directs': directs,
            'active_direct': active_direct,
            'messages': messages,
            'request': request,
            'to': to
        }
          
    return render(request, 'directs/test_direct.html', context)
    
    
def SendMessage(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')
    
    if request.method == "POST":
        if body == '':
            print(f'пусто')
            to_user = User.objects.get(username=to_user_username)
            if to_user == from_user:
                
                return redirect(request.META.get('HTTP_REFERER'))
            Message.send_message(from_user, to_user, body)
            
            return redirect(request.META.get('HTTP_REFERER'))
        elif to_user_username == None:
            print('нет получателя')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            if to_user_username == None:
                print('нет получателя')
            to_user = User.objects.get(username=to_user_username)
            if to_user == from_user:
                
                return redirect(request.META.get('HTTP_REFERER'))
            
            Message.send_message(from_user, to_user, body)
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        
        return redirect(request.META.get('HTTP_REFERER'))
        
def UserSearch(request):
    query = request.GET.get('q')
    context = {}
    if query:
        users = User.objects.filter(Q(username__icontains=query))
        
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)
        
        context = {
            'users': users_paginator,
        }
        
    return render(request, 'directs/search.html', context) 