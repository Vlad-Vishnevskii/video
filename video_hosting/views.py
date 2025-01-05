# -*- coding: utf-8 -*-
import json
from django.contrib.auth.decorators import login_required


from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from .backends import *
from .models import *
from .services import open_file
from .forms import ArticleForm, ArticleForm1, AuthUserForm, RegisterUserForm, CommentForm, EditeProfileForm, ArticleForm2, ArticleForm3, ArticleForm4, ArticleForm5, ArticleForm6, ArticleForm7, ArticleForm8, ArticleForm9, ArticleForm10, ArticleForm11
from django.views import View
from django.db import transaction
import random
from datetime import datetime

from django.db.models.functions import Now
import os
from django.views.decorators.csrf import ensure_csrf_cookie
import math
from PIL import Image
import numpy
import moviepy.editor as mp
from datetime import date
from moviepy.editor import *



def get_list_video(request):
    # video_list = Video.objects.order_by('-likes')[:10]
    random_items = list(Video.objects.all())
    #if len(random_items) > 1:
    video_list = random.sample(random_items, 1)
    #elif len(random_items) > 5:
        #video_list = random.sample(random_items, 5)
   

    context = {
        'video_list': video_list
    }

    return render(request, 'video_hosting/test_home.html', context)
def get_list_dance(request):
    # video_list = Video.objects.order_by('-likes')[:10]
    random_items = list(Video.objects.all())
    #if len(random_items) > 1:
    video_list = random.sample(random_items, 1)
    #elif len(random_items) > 5:
    m = video_list[0]
    y = m.author
        #video_list = random.sample(random_items, 5)
   
    
    context = {
        'video_list': video_list, 
        'y': y,
    }

    return render(request, 'video_hosting/seedance.html', context)    
    
    

def examples(request):
    # video_list = Video.objects.order_by('-likes')[:10]
    random_items = list(Video.objects.all())
    if len(random_items) < 6 and len(random_items) > 0:
        video_list = random.sample(random_items, len(random_items))
    elif len(random_items) > 5:
        video_list = random.sample(random_items, 5)
    else:
        video_list = []

    context = {
        'video_list': video_list
    }

    return render(request, 'video_hosting/examples.html', context)

def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response
    
class CustomSuccessMessageMixin:
    
    @property
    def success_msg(self):
        return False
    
    def form_valid(self,form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
        
    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)
        
        
# view profile
def ViewProfile(request, pk : int):
    user = request.user
    video_list = Video.objects.filter(author=request.user.id)
    context = {
       'user': user,
       'video_list': video_list, 
    }
    if not request.user.is_authenticated:
        return redirect('login')
    else:
    
        return render(request, 'video_hosting/user_profile.html', context)
    
def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    return age
        
def Profile(request, username):
    video = Video
    current_user = request.GET.get('username')
    logged_in_user = request.user.username
    current_user_id = request.user.id
    user = get_object_or_404(User, username=username)
    video_list = Video.objects.filter(author=user.id)
    birdday = user.birdday
    age = calculate_age(user.birdday)

    print(f"Current user from GET: {current_user}")
    
    # статистика пользователя
    post_count = Video.objects.filter(author=user.id).count()
    following_count = FollowersCount.objects.filter(user=user).count()
    followers_count = FollowersCount.objects.filter(follower=user).count()
    
    follow_status = FollowersCount.objects.filter(follower=user, user=request.user).exists()
    is_request_meet_enable = not MeetingRequest.objects.filter(from_user=current_user_id, to_user=user, status__in=["send", "accepted"]).exists()
    
    context = {
       'user': user,
       'birdday': birdday,
       'age': age,
       'video_list': video_list,
       'current_user': current_user, 
       'logged_in_user' : logged_in_user,
       'post_count' : post_count,
       'following_count' : following_count, 
       'followers_count' : followers_count, 
       'follow_status' : follow_status,
       'is_request_meet_enable' : is_request_meet_enable,
    }
    if not request.user.is_authenticated:
        return render(request, 'video_hosting/test_profile.html', context)
    else:
    
        return render(request, 'video_hosting/test_profile.html', context)
        

def verifyprofile(username):
    user = username
    user = get_object_or_404(User, username=username)
    today = datetime.today().strftime('%Y-%m-%d')
    a = user.finish_month
    a = str(a).split(' ')[0]
    print(a)
    print(today)
    if today > a:
        
        user.is_verified = False
        user.save()
    else:
        user.is_verified = True
        user.save()

def wallet_user(request, username):
    user = get_object_or_404(User, username=username)
    try:
        if request.user.username == user.username:
            if request.method == 'GET':
                counts = get_wallet(username)
                return render(request, 'video_hosting/wallet.html', context={'money': counts})
            else:
                code = request.POST.get('code')
                res = end_check(code, request.user.username)
                if res:
                    return redirect('/success/success_payment')
                else:
                    return redirect('/error/code')

        else:
            return redirect(f'/profile/{request.user.username}/wallet/')
    except:
        return redirect('/error/code1')


def send_coins_page(request):
    if request.method == 'GET' and request.user.is_authenticated:
        counts = get_wallet(request.user)
        return render(request, 'video_hosting/sendmoney.html', context={'money': counts})
    elif request.method == 'POST' and request.user.is_authenticated:
        to_user = request.POST.get('to_name', None)
        email = request.POST.get('email', None)
        money = request.POST.get('count', None)
        username = request.user.username
        res = send_money(to_user, email, money, username)
        if res:
            return redirect('/success/success_send')

        else:
            return redirect('/error/error_send')

    return redirect('/login')
    
def send_stars_page(request):
    if request.method == 'GET' and request.user.is_authenticated:
        counts = get_wallet(request.user)
        return render(request, 'video_hosting/sendstar.html', context={'money': counts})
    elif request.method == 'POST' and request.user.is_authenticated:
        to_user = request.POST.get('to_name', None)
        email = request.POST.get('email', None)
        money = request.POST.get('count', None)
        username = request.user.username
        res = send_money(to_user, email, money, username)
        if res:
            return redirect('/success/success_send')

        else:
            return redirect('/error/error_send')

    return redirect('/login')

def status_sending(request, status):
    if request.user.is_authenticated:
        if status == 'success_send':
            return render(request, 'video_hosting/succec.html',
                          context={'title': 'Успешный перевод', 'descr': 'Вы перевели средства другому пользователю!',
                                   'url': f'/profile/{request.user.username}/wallet'
                                   })
        elif status == 'success_payment':
            return render(request, 'video_hosting/succec.html',
                          context={'title': 'Успешная оплата!', 'descr': 'Вы уже получили средства на свой счет :)!',
                                   'url': f'/profile/{request.user.username}/wallet'
                                   })
        
    return redirect('/error/what')

def error_wallet(request, status):
    if request.user.is_authenticated:
        if status == 'error_send':
            return render(request, 'video_hosting/error.html',
                          context={'descr': 'Данные введенные вами не верны, или у вас не достаточно средств',
                                   'url': f'/profile/{request.user.username}/wallet'
                                   })
        elif status == 'what':
            return render(request, 'video_hosting/error.html',
                          context={'descr': 'Возможно вы потерялись',
                                   'url': '/'
                                   })
        elif status == 'code':
            return render(request, 'video_hosting/error.html',
                          context={'descr': 'Ваш код оплаты был уже введен!',
                                   'url': f'/profile/{request.user.username}/wallet'
                                   })
        elif status == 'code1':
            return render(request, 'video_hosting/error.html',
                          context={'descr': 'Неверный код!',
                                   'url': f'/profile/{request.user.username}/wallet'
                                   })
    return redirect(f'/profile/{request.user.username}/wallet')


@csrf_exempt
def getting_checks(req):
    money = req.POST.get('money')
    check = req.POST.get('check')
    create_check(check, float(money))
    return HttpResponse('Created')

def follow(request, username, option):
    user = request.user
    follower = get_object_or_404(User, username=username)
    if request.user == user.username:
        return HttpResponseRedirect(reverse('profile', args=[username]))
    try:
        f, created = FollowersCount.objects.get_or_create(user=request.user, follower=follower)

        if int(option) == 0:
            f.delete()
        return HttpResponseRedirect(reverse('profile', args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))
    

@login_required
def send_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        MeetingRequest.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, 'Post True!')
        return redirect('directs', to_user)  
    return render(request, 'video_hosting/send_request.html', {'to_user': to_user})

@login_required
def respond_request(request, request_id, action):
    meeting_request = get_object_or_404(MeetingRequest, id=request_id, to_user=request.user)
    if action == 'accept':
        meeting_request.status = 'accepted'
        meeting_request.save()
        messages.success(request, 'True!')
    elif action == 'decline':
        meeting_request.status = 'declined'
        meeting_request.save()
        messages.success(request, 'False!')
    else:   
        return HttpResponseRedirect(reverse('profile', args=[username]))
    return render(request, 'test_home.html')

@login_required
def handle_request(request):
    # Получить параметры из запроса
    action = request.GET.get('action')
    user_id = request.GET.get('user_id')

    # Найти запрос в базе данных
    meeting_request = get_object_or_404(MeetingRequest, from_user_id=user_id, to_user=request.user)

    if action == 'accept':
        # Логика для принятия запроса
        meeting_request.status = 'accepted'
        meeting_request.save()
        return JsonResponse({'status': 'success', 'message': f'Запрос от пользователя {meeting_request.from_user} принят.'})
    elif action == 'decline':
        # Логика для отклонения запроса
        meeting_request.status = 'declined'
        meeting_request.save()
        return JsonResponse({'status': 'success', 'message': f'Запрос от пользователя {meeting_request.from_user} отклонен.'})
    else:
        # Если action неизвестен
        return JsonResponse({'status': 'error', 'message': 'Некорректное действие.'}, status=400)     
    

# edit profile
class Edite(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = User
    template_name = 'video_hosting/edit_user_profile.html'
    form_class = EditeProfileForm
    success_url = reverse_lazy('createmusic')
    success_msg = 'Данные обновлены'
    
    def get_context_data(self, **kwargs):
            kwargs['update'] = True
            return super().get_context_data(**kwargs)
        
       
        
        
        
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip     

class VideoDetailView(DetailView):
    model = Video
    template_name = 'video_hosting/videomain.html'
    content_object_name = 'post'
    form_class = CommentForm
    success_msg = "Комментарий добавлен"
    
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        ip = get_client_ip(self.request)
        print(ip)
        if IpModel.objects.filter(ip=ip).exists():
            print("ip already present")
            video_id = request.GET.get('video.id')
            print(video_id)
            post = Video.objects.get(pk=video_id)
            post.views.add(IpModel.objects.get(ip=ip))
        else:
            IpModel.objects.create(ip=ip)
            video_id = request.GET.get('video.id')
            post = Video.objects.get(pk=video_id)
            post.views.add(IpModel.objects.get(ip=ip))
        return self.render_to_response(context)
        
        
class VideoDetailView(CustomSuccessMessageMixin, FormMixin, DetailView):
    model = Video
    template_name = 'video_hosting/videomain.html'
    content_object_name = 'video_list'
    form_class = CommentForm
    success_msg = "Комментарий добавлен"
    
    
    
    def get_context_data(self, **kwargs):
        kwargs['video_list'] = Video.objects.all()  
        return super().get_context_data(**kwargs)
       
    def get_success_url(self, **kwargs):
        return reverse_lazy('videomain', kwargs={'pk': self.get_object().id})
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
     
    
        
"""
class VideoCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    model = Video
    template_name = 'video_hosting/create.html'
    form_class = ArticleForm
    success_url = reverse_lazy('create')
    success_msg = 'Запись создана'
    def get_context_data(self, **kwargs):
        kwargs['list_video'] = Video.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)
        
       
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
#        video_quality(str(self.object.file))
        return super().form_valid(form)
"""        
""" video_input_path = '/your/video.mp4'
                img_output_path = '/your/image.jpg'
                subprocess.call(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes', '1', img_output_path])
                """


def video_create(request):
    user = request.user
    if request.method == "POST":
        video_file = request.FILES.get('video')  # Получаем один видеофайл
        # Создаем новый объект Video
        new_video = Video(file=video_file, author=user)
        new_video.save()
        try:
            # Генерация случайного числа для имени изображения
            random_string = random.randint(10000, 99999)
            video_input_path = f'{BASE_DIR}/media/{new_video.file}'
            img_output_path = f'/home/django/django_venv/src/media/video/{random_string}.jpg'
            
            # Генерация превью с помощью ffmpeg
            subprocess.call(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes', '1', img_output_path])

            new_video.image = f'video/{random_string}.jpg'

            new_video.save()
        except:
           # Генерация случайного числа для имени изображения
            random_string = random.randint(10000, 99999)
            video_input_path = f'{BASE_DIR}/media/{new_video.file}'
            img_output_path = f'/home/django/django_venv/src/media/video/{random_string}.jpg'
            
            # Генерация превью с помощью ffmpeg
            subprocess.call(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes', '1', img_output_path])

            new_video.image = f'video/{random_string}.jpg'

            new_video.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    return render(request, "video_hosting/createvideoform.html")

    
#@ensure_csrf_cookie
def slideshow(request):
    user = request.user
    finish = str(user.finish_month)
    finish = str(finish).split(' ')[0]
    if request.method == 'POST':
        form = ArticleForm9(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        print(files)
        file_list = []
        if form.is_valid():
            
            for file in files:
                new_file = SlideshowCreate(
                file=file, authors8=user)
                d = str(new_file.p)
                name = new_file.authors8
                video = new_file.file
                print(name)
                print(d)
                video_path = f'{BASE_DIR}/media/skideshow/{d}'
        # v = Video.objects.create(file=file)
                new_file.save()
                file_list.append(new_file) 
                
        try:
            re_rend_video8(request, user, video_path)
            form = ArticleForm9()
            slide = Slideshow.objects.all().order_by('-id')
            context = {'form': form, 'slide': slide, 'finish':finish, 'aler_flag': True}
            return render(request, 'video_hosting/slideshow.html', context)
        except:
            form = ArticleForm9()
            slide = Slideshow.objects.all().order_by('-id')
            context = {'form': form, 'slide': slide, 'finish':finish, 'alert_flag': True}
            return render(request, 'video_hosting/slideshow.html', context)
            
    form = ArticleForm9()
    slide = Slideshow.objects.all().order_by('-id')
    context = {'form': form, 'slide': slide, 'finish':finish}
    
    return render(request, 'video_hosting/slideshow.html', context)
    
def process_data8(request):
    if request.method == 'POST':
        print(request)
        files = request.FILES.getlist('files')
        print(files)
        for file in files:
            if file != None:
            
                user = User.objects.filter(username=request.user).first()
                aud1 = SlideshowCreate.objects.create(authors8=user, file=file)
                print(user)
                print(audio)
                print(file)
                aud1.save()
                # vid.authors = request.user
                print(aud1)
                # Здесь получаем запрос и сохраняем видео, без доп музыки и прочего
                return JsonResponse({'file': str(aud1.file)})
        else:
            print('adwd')
                
    else:
        return redirect('/slideshow')

def re_rend_video8(request, name, video_path):
    if request.method == 'POST':
        user = name
        finish = str(user.finish_month)
        finish = str(finish).split(' ')[0]
        vid1 = SlideshowCreate.objects.filter(authors8=name).first()
        print(vid1)
        sladeshow(video_path, user, video_path)
        
        form = ArticleForm9()
        slide = Slideshow.objects.all().order_by('-id')
        context = {'form': form, 'slide': slide, 'finish':finish, 'aler_flag': True}
        return render(request, 'video_hosting/slideshow.html', context)


        
def videoshow(request):
    user = request.user
    #finish = str(user.finish_month)
    #finish = str(finish).split(' ')[0]
    name = None
    video_path = None   
    if request.method == 'POST':
        user = request.user
        form = ArticleForm10(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        print(files)
        
        
        file_list = []
        
        if form.is_valid():
            
            
            for file in files:
                new_file = VideoshowCreate(
                file=file, authors10=user)
                d = str(new_file.p)
                name = new_file.authors10
                video = new_file.file
                print(name)
                print(file)
                video_path = f'{BASE_DIR}/media/videoshow/{d}'
        # v = Video.objects.create(file=file)
                new_file.save()
                file_list.append(new_file) 
        
    if name or video_path == '':
        messages.success(request, 'Готовый файл можно будет скачать позже')
        re_rend_video9(request, user, video_path)
        form = ArticleForm10()
        slide1 = Videoshow.objects.all().order_by('-id')
        context = {'form': form, 'slide1': slide1, 'aler_flag': True}
        return render(request, 'video_hosting/videoshow.html', context)
    else:
        messages.success(request, 'Не выбраны файлы')
        re_rend_video9(request, user, video_path)    
        form = ArticleForm10()
        slide1 = Videoshow.objects.all().order_by('-id')
        context = {'form': form, 'slide1': slide1, 'alert_flag': True}
        return render(request, 'video_hosting/videoshow.html', context)
    
                
       
    form = ArticleForm10()
    slide1 = Videoshow.objects.all().order_by('-id')
    context = {'form': form, 'slide1': slide1}
    
    return render(request, 'video_hosting/videoshow.html', context)


 
def re_rend_video9(request, name, video_path):
    
    user = name
    videoshow1(video_path, user, video_path)
    form = ArticleForm10()
    slide1 = Videoshow.objects.all().order_by('-id')
    context = {'form': form, 'slide1': slide1, 'aler_flag': True}
    return render(request, 'video_hosting/videoshow.html', context)

class VideoCreateMusic(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    model = VideoCreate
    template_name = 'video_hosting/test_createmusic.html'
    form_class = ArticleForm1
    success_url = reverse_lazy('createmusic')
    success_msg = 'Замена музыки запущена, подождите 5 минут страница обновится и можно скачать готовый файл, если нажать сразу скачать скачается исходный файл'
    
    
    def get_context_data(self, **kwargs):
        kwargs['list_videocreate'] = VideoCreate.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)

    # @audio_dec
    def form_valid(self,form):
        obj = form.save(commit=False)
        print(obj)
        return redirect('/loading')
    
        
class MusicCreate(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    model = AudioCreate
    template_name = 'video_hosting/audiochange.html'
    form_class = ArticleForm2
    success_url = reverse_lazy('audiocut')
    success_msg = 'Замена музыки запущена, подождите 5 минут страница обновится и можно скачать готовый файл, если нажать сразу скачать скачается исходный файл'
    
    
    def get_context_data(self, **kwargs):
        kwargs['list_audiocreate'] = AudioCreate.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)

    # @audio_dec
    def form_valid(self,form):
        obj = form.save(commit=False)
        print(obj)
        return redirect('/loading1')

    # def form_valid(self, form):
    #     tasks.add_music.delay()
    #     self.object = form.save(commit=False)
    #     Audio.objects.create(audio_path=self.object.audio)
    #     self.object.authors = self.request.user
    #     self.object.save()
    #     messages.success(self.request, '')
    #     return super().form_valid(form)

def video_create_music(request):
    user = request.user
    username = user
    verifyprofile(username)
    finish = str(user.finish_month)
    finish = str(finish).split(' ')[0]
    if request.method == 'POST':
        form = ArticleForm1(request.POST, request.FILES)
        if form.is_valid():
            file_value = request.FILES.get('file', None)
            music_value = request.FILES.get('audio', None)
            start_value = request.POST.get('start', None)
            
            initial_data = {'file': file_value, 'audio': music_value, 'start': start_value}
            form = ArticleForm1(initial=initial_data)
            
        return render(request, 'video_hosting/loading.html', context={'form': form})

    form = ArticleForm1()
    #list_videocreate = VideoCreate.objects.all().order_by('-id')
    list_videocreate = VideoCreate.objects.exclude(file="", audio="")
    list_videocreate1 = []
    print(list_videocreate)
    
    context = {'form': form, 'list_videocreate': list_videocreate, 'finish': finish}
    
    return render(request, 'video_hosting/test_createmusic.html', context)

def process_data(request):
    if request.method == 'POST':
            
        video_file = request.FILES.get('file')
        audio_file = request.FILES.get('audio')
        start = request.POST.get('start')
        if video_file == '' or audio_file == '':
            return redirect('/createmusic')
        else:
        
            user = User.objects.filter(username=request.user).first()
            vid = VideoCreate(file=video_file, audio=audio_file, authors=user, start=start)
                # vid.authors = request.user
            vid.save()
                # Здесь получаем запрос и сохраняем видео, без доп музыки и прочего
            return JsonResponse({'file': str(vid.file), 'audio': str(vid.audio), 'start': str(vid.start)})
            
        
    else:
        return redirect('/createmusic')

def re_rend_video(request):
    if request.method == 'POST':
        video_file = request.POST.get('file')
        audio_file = request.POST.get('audio')
        start_file = request.POST.get(str('start'))
        if video_file == '' or audio_file == '':
            messages.success(request, 'Не выбран видео или аудио файл')
            
        else:
            vid = VideoCreate.objects.filter(file=video_file).first()
            print(vid.file, video_file, vid.audio, vid.start)
            audio_change_back_proc(video_file, vid.audio, vid.start) # замена аудио
            return redirect('/createmusic')
        
        
def audio_create(request):
    user = request.user
    finish = str(user.finish_month)
    finish = str(finish).split(' ')[0]
    
    if request.method == 'POST':
        form = ArticleForm2(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES.get('audio')
            print(audio_file)
            start = request.POST.get(str('start'))
            print(start)
            finish = request.POST.get('finish')
            print(finish)
            data=form.cleaned_data
            form.save()
            return redirect('video_hosting/error1.html')
        else:
            return redirect('video_hosting/error1.html')
    else:
        form = ArticleForm2()
    
    form = ArticleForm2()
    list_audiocreate = AudioCreate.objects.all().order_by('-id')
    context = {'form': form, 'list_audiocreate': list_audiocreate, 'finish': finish}
    
    return render(request, 'video_hosting/audiochange.html', context)
    

def error_wallet1(request):
    if request.user.is_authenticated:
        return render(request, 'video_hosting/error1.html')
        
def process_data1(request):
    
    if request.method == 'POST':
            
        audio_file = request.FILES.get('audio')
        print(audio_file)
        start = request.POST.get(str('start'))
        print(start)
        finish = request.POST.get('finish')
        print(finish)
            
        user = User.objects.filter(username=request.user).first()
        aud = AudioCreate.objects.create(audio=audio_file, authors1=user, start=start, finish=finish)
        print(user)
        print(audio_file)
        print(start)
        print(finish)
        aud.save()
                # vid.authors = request.user
                
                # Здесь получаем запрос и сохраняем видео, без доп музыки и прочего
        return JsonResponse({'audio': str(aud.audio), 'start': aud.start, 'finish': aud.finish})
    else:
        return redirect('/audiocut')
        
        
def re_rend_video1(request):
    
    if request.method == 'POST':
        audio_file = request.POST.get('audio')
            
        start_value = request.POST.get('start')
        finish_value = request.POST.get('finish')
            
            
            
        aud = AudioCreate.objects.filter(audio=audio_file, start=start_value, finish=finish_value).first()
       
        audio_cut(aud.audio, aud.start, aud.finish)
                # замена аудио
        return redirect('/audiocut')
    else:
        return redirect('/audiocut')


def reels_create(request):
    user = request.user
    finish = str(user.finish_month)
    finish = str(finish).split(' ')[0]
    if request.method == 'POST':
        form = ArticleForm3(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES.get('audio', None)
            video_file = request.FILES.get('file', None)
            initial_data = {'file': video_file, 'audio': audio_file}
            form = ArticleForm3(initial=initial_data)
            form.save()
        return render(request, 'video_hosting/reels.html', context={'form': form})
        
    
    form = ArticleForm3()
    reels = ReelsCreate.objects.all().order_by('-id')
    context = {'form': form, 'reels': reels, 'finish':finish}
    
    return render(request, 'video_hosting/reels.html', context)
    
def process_data2(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        audio = request.FILES.get('audio')
        if file or audio != None:
        
            user = User.objects.filter(username=request.user).first()
            aud1 = ReelsCreate.objects.create(authors2=user, file=file, audio=audio)
            print(user)
            print(audio)
            print(file)
            aud1.save()
            # vid.authors = request.user
            print(aud1)
            # Здесь получаем запрос и сохраняем видео, без доп музыки и прочего
            return JsonResponse({'file': str(aud1.file), 'audio': str(aud1.audio)})
    else:
        return redirect('/reels')

def re_rend_video2(request):
    if request.method == 'POST':
        video_file = request.POST.get('file')
        audio_file = request.POST.get('audio')
        vid1 = ReelsCreate.objects.filter(file=video_file, audio=audio_file).first()
        print(video_file, vid1.audio)
        video_back_proc(vid1.audio, vid1.file) # замена аудио
        return redirect('/reels')
        
        
        

def zip_image(request):
    user = request.user
    finish = str(user.finish_month)
    finish = str(finish).split(' ')[0]
    if request.method == 'POST':
        form = ArticleForm4(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES.get('file', None)
            initial_data = {'file': video_file}
            form = ArticleForm4(initial=initial_data)
            form.save()
        return render(request, 'video_hosting/images.html', context={'form': form})
    
    form = ArticleForm4()
    images = ImagesCreate.objects.all().order_by('-id')
    context = {'form': form, 'images': images, 'finish':finish}
    
    return render(request, 'video_hosting/images.html', context)
    
def process_data3(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file != None:
        
            user = User.objects.filter(username=request.user).first()
            aud1 = ImagesCreate.objects.create(authors3=user, file=file)
            print(user)
            print(file)
            aud1.save()
            # vid.authors = request.user
            print(aud1)
            # Здесь получаем запрос и сохраняем видео, без доп музыки и прочего
            return JsonResponse({'file': str(aud1.file)})
    else:
        return redirect('/images')

def re_rend_video3(request):
    if request.method == 'POST':
        video_file = request.POST.get('file')
        vid1 = ImagesCreate.objects.filter(file=video_file).first()
        print(video_file)
        images_back_proc(vid1.file) # замена аудио
        return redirect('/images')
        
        
def blackwhite(request):
    user = request.user
    finish = str(user.finish_month)
    finish = str(finish).split(' ')[0]
    if request.method == 'POST':
        form = ArticleForm5(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES.get('file', None)
            initial_data = {'file': video_file}
            form = ArticleForm5(initial=initial_data)
            form.save()
        return render(request, 'video_hosting/blackwhite.html', context={'form': form})
    
    form = ArticleForm5()
    bw = BwCreate.objects.all().order_by('-id')
    context = {'form': form, 'bw': bw, 'finish':finish}
    
    return render(request, 'video_hosting/blackwhite.html', context)
    
def process_data4(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file != None:
        
            user = User.objects.filter(username=request.user).first()
            aud1 = BwCreate.objects.create(authors4=user, file=file)
            print(user)
            print(file)
            aud1.save()
            # vid.authors = request.user
            print(aud1)
            # Здесь получаем запрос и сохраняем видео, без доп музыки и прочего
            return JsonResponse({'file': str(aud1.file)})
    else:
        return redirect('/blackwhite')

def re_rend_video4(request):
    if request.method == 'POST':
        video_file = request.POST.get('file')
        vid1 = BwCreate.objects.filter(file=video_file).first()
        print(video_file)
        blackwhite_back_proc(vid1.file) # замена аудио
        return redirect('/blackwhite')

def slowing(request):
    user = request.user
    finish = str(user.finish_month)
    finish = str(finish).split(' ')[0]
    if request.method == 'POST':
        form = ArticleForm6(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES.get('file', None)
            initial_data = {'file': video_file}
            form = ArticleForm6(initial=initial_data)
            form.save()
        return render(request, 'video_hosting/slowing.html', context={'form': form})
    
    form = ArticleForm6()
    slowing = SlowingCreate.objects.all().order_by('-id')
    context = {'form': form, 'slowing': slowing, 'finish':finish}
    
    return render(request, 'video_hosting/slowing.html', context)
    
def process_data5(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file != None:
        
            user = User.objects.filter(username=request.user).first()
            aud1 = SlowingCreate.objects.create(authors5=user, file=file)
            print(user)
            print(file)
            aud1.save()
            # vid.authors = request.user
            print(aud1)
            # Здесь получаем запрос и сохраняем видео, без доп музыки и прочего
            return JsonResponse({'file': str(aud1.file)})
    else:
        return redirect('/blackwhite')

def re_rend_video5(request):
    if request.method == 'POST':
        video_file = request.POST.get('file')
        vid1 = SlowingCreate.objects.filter(file=video_file).first()
        print(video_file)
        slowing_back_proc(vid1.file) # замена аудио
        
        return redirect('/blackwhite')  



def speedup(request):
    user = request.user
    finish = str(user.finish_month)
    finish = str(finish).split(' ')[0]
    if request.method == 'POST':
        form = ArticleForm11(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES.get('file', None)
            initial_data = {'file': video_file}
            form = ArticleForm11(initial=initial_data)
            form.save()
        return render(request, 'video_hosting/speedup.html', context={'form': form})
    
    form = ArticleForm11()
    slowing = SpeedCreate.objects.all().order_by('-id')
    context = {'form': form, 'slowing': slowing, 'finish':finish}
    
    return render(request, 'video_hosting/speedup.html', context)
    
def process_data10(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file != None:
        
            user = User.objects.filter(username=request.user).first()
            aud1 = SpeedCreate.objects.create(authors12=user, file=file)
            print(user)
            print(file)
            aud1.save()
            # vid.authors = request.user
            print(aud1)
            # Здесь получаем запрос и сохраняем видео, без доп музыки и прочего
            return JsonResponse({'file': str(aud1.file)})
    else:
        return redirect('/blackwhite')

def re_rend_video10(request):
    if request.method == 'POST':
        video_file = request.POST.get('file')
        vid1 = SpeedCreate.objects.filter(file=video_file).first()
        print(video_file)
        speed_back_proc(vid1.file) # замена аудио
        
        return redirect('/blackwhite')  
    

def render_video(request):
    user = request.user
    if request.method == 'POST':
        print(user)
        form = ArticleForm7(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES.get('file', None)
            initial_data = {'file': video_file}
            form = ArticleForm7(initial=initial_data)
            form.save()
        return render(request, 'video_hosting/render.html', context={'form': form})
    
    form = ArticleForm7()
    render1 = RenderCreate.objects.all().order_by('-id')
    finish = str(user.finish_month)
    finish = str(finish).split(' ')[0]
    context = {'form': form, 'render1': render1, 'finish': finish}
    
    return render(request, 'video_hosting/render.html', context)  

def process_data6(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file != None:
        
            user = User.objects.filter(username=request.user).first()
            aud1 = RenderCreate.objects.create(authors6=user, file=file)
            print(user)
            print(file)
            aud1.save()
            # vid.authors = request.user
            print(aud1)
            # Здесь получаем запрос и сохраняем видео, без доп музыки и прочего
            return JsonResponse({'file': str(aud1.file)})
    else:
        return redirect('/render')

def re_rend_video6(request):
    if request.method == 'POST':
        video_file = request.POST.get('file')
        vid1 = RenderCreate.objects.filter(file=video_file).first()
        print(video_file)
        render_back_proc(vid1.file) # замена аудио
        return redirect('/render')      



def render_vid(request):
    user = request.user
    if request.method == 'POST':
        form = ArticleForm8(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES.get('file', None)
            initial_data = {'file': video_file}
            form = ArticleForm8(initial=initial_data)
            form.save()
        return render(request, 'video_hosting/render1.html', context={'form': form})
    
    form = ArticleForm8()
    render2 = RendCreate.objects.all().order_by('-id')
    finish = str(user.finish_month)
    finish = str(finish).split(' ')[0]
    context = {'form': form, 'render2': render2, 'finish': finish}
    
    return render(request, 'video_hosting/render1.html', context)  

def process_data7(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file != None:
        
            user = User.objects.filter(username=request.user).first()
            aud1 = RendCreate.objects.create(authors7=user, file=file)
            print(user)
            print(file)
            aud1.save()
            # vid.authors = request.user
            print(aud1)
            # Здесь получаем запрос и сохраняем видео, без доп музыки и прочего
            return JsonResponse({'file': str(aud1.file)})
    else:
        return redirect('/render1')

def re_rend_video7(request):
    if request.method == 'POST':
        video_file = request.POST.get('file')
        vid2 = RendCreate.objects.filter(file=video_file).first()
        print(video_file)
        render1(vid2.file) # замена аудио
        return redirect('/render1')    
        



class UpdateCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = Video
    template_name = 'video_hosting/create.html'
    form_class = ArticleForm
    success_url = reverse_lazy('create')
    success_msg = 'Запись успешно обновлена'
    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)
        
        
def delete_video_v(request, pk: int):
    try:
        
        delete_video(pk)
        return redirect('/create')
    except:
        return redirect('/create')
        
        
    

def download_video_v(request, pk: int):
    return download_video(pk)
    
def delete_video_w(request, pk: int):
    delete_video_r(pk)
    return redirect('/createmusic')

def download_video_f(request, pk: int):
    return download_video1(pk)
    
def download_video_w(request, pk: int):
    return download_video3(pk)
    
def download_audio_w(request, pk: int):
    return download_audio(pk)
    
def download_video_z(request, pk: int):
    return download_video2(pk)
    

    
def download_slide_w(request, pk: int):
    return download_slide(pk)

def download_slide_f(request, pk: int):
    return download_slide1(pk)

def download_images(request, pk: int):
    return download_zip_image(pk)
    
def download_blackwhite(request, pk: int):
    return download_blackwhite1(pk)
 
def download_render(request, pk: int):
    return download_render3(pk)
    
def download_render1(request, pk: int):
    return download_render2(pk)
    
def download_slowing(request, pk: int):
    return download_slowing1(pk)

def download_speed(request, pk: int):
    return download_speed1(pk)

class MyprojectLoginView(LoginView):
    template_name = 'video_hosting/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('createmusic')
    def get_success_url(self):
        return self.success_url
    
class RegisterUserView(CreateView):
    model = User
    template_name = 'video_hosting/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('createmusic')
    success_msg = 'Пользователь успешно создан'
    
    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        birdday = form.cleaned_data["birdday"]
        gender = form.cleaned_data["gender"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        create_wallet(username)
        return form_valid
        

class MyprojectLogoutView(LogoutView):
    next_page = reverse_lazy('home')
    
class AddLike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        post = Video.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break


        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        return HttpResponseRedirect(reverse('videomain', args=[str(pk)]))



class AddDislike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        post = Video.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)



        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        return HttpResponseRedirect(reverse('videomain', args=[str(pk)]))
        




