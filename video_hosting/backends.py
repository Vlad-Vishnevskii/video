#!/bin/sh

import os
import random
import time
import glob
from django.db import transaction, connection
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from video_hosting import notisend
from moviepy.editor import *
import sys
import subprocess
from video_hosting.models import *
from django_project.settings import BASE_DIR
import datetime

project = 'test_name'  # Имя проекта
api_key = 'db1716d1afe906ae2dee1e4365b2dcc3'  # API-ключ

# Создаём объект
sms = notisend.SMS(project, api_key)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
           return User.objects.get(pk=user_id)
        except User.DoesNotExist:
           return None

    def authenticate(self, request, username, password):

        try:
            user = User.objects.get(
                Q(username=username) | Q(email=username) | Q(phone=username)
            )

        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        else:
            return None


def create_wallet(username):
    user = User.objects.get(username=username)
    WalletUser.objects.create(user_id=user.id)
    user1 = user.date_joined
    user.finish_month = user1 + datetime.timedelta(days=7)
    user.is_verified = True
    user.save()
    


def get_wallet(username):
    user = User.objects.get(username=username)
    wall = WalletUser.objects.get(user_id=user.id)
    return wall.condition

@transaction.atomic
def send_money(to_user, money, username):
    user = User.objects.get(username=username)
    cond = get_wallet(username)
    if float(cond) >= float(money) and User.objects.filter(username=to_user).exists():
            wall = WalletUser.objects.get(user_id=user.id)
            wall.condition -= float(money)
            user_to = User.objects.get(username=to_user)
            wall_to = WalletUser.objects.get(user_id=user_to.id)
            wall_to.condition += float(money)
            if wall == wall_to:
                print('перевести себе не получится')
                return False
            else:
                wall.save()
                wall_to.save()
                return True
    
    else:
        print('перевести себе не получится')
        return False

def create_check(check, money):
    check = Check.objects.create(check_info=check, money=money)
    check.save()

@transaction.atomic
def end_check(code, username):
    check = Check.objects.get(check_info=code)
    if not check.status:
        user = User.objects.get(username=username)
        wall = WalletUser.objects.get(user_id=user.id)
        check.status = True
        wall.condition += check.money
        check.save()
        wall.save()
        return True
    else:
        return False

def delete_video(id):
    v = Video.objects.get(id=id)
    os.remove(f'{BASE_DIR}/media/{str(v.file)}')
    with connection.cursor() as cursor:
        cursor.execute(f'DELETE FROM video_hosting_video WHERE id = {id};')

def delete_video_r(id):
    w = VideoCreate.objects.get(id=id)
    os.remove(f'{BASE_DIR}/media/{str(w.file)}')
    with connection.cursor() as cursor:
        cursor.execute(f'DELETE FROM video_hosting_video WHERE id = {id};')


def download_video(id):
    v = Video.objects.get(id=id)
    return FileResponse(open(f'media/{str(v.file)}', 'rb'))

def download_video3(id):
    w = VideoCreate.objects.get(id=id)
    return FileResponse(open(f'media/{str(w.file)}', 'rb'))
 
def download_video2(id):
    w = ReelsCreate.objects.get(id=id)
    return FileResponse(open(f'media/{str(w.file)}', 'rb'))
 
def download_zip_image(id):
    a = ImagesCreate.objects.get(id=id)
    return FileResponse(open(f'{str(a.file)}', 'rb'))

def download_blackwhite1(id):
    b = BwCreate.objects.get(id=id)
    return FileResponse(open(f'{str(b.file)}', 'rb'))
   
   
def download_slowing1(id):
    c = SlowingCreate.objects.get(id=id)
    return FileResponse(open(f'{str(c.file)}', 'rb'))
    
def download_speed1(id):
    s = SpeedCreate.objects.get(id=id)
    return FileResponse(open(f'{str(s.file)}', 'rb'))
    
def download_slide(id):
    slide = SlideshowCreate.objects.get(id=id)
    return FileResponse(open(f'{str(slide.file)}', 'rb'))
    
def download_slide1(id):
    slide = Slideshow.objects.get(id=id)
    return FileResponse(open(f'{str(slide.file)}', 'rb'))

def download_video1(id):
    f = Videoshow.objects.get(id=id)
    return FileResponse(open(f'{str(f.file)}', 'rb'))
    
def download_render3(id):
    p = RenderCreate.objects.get(id=id)
    return FileResponse(open(f'{str(p.file)}', 'rb'))

def download_render2(id):
    s = RendCreate.objects.get(id=id)
    return FileResponse(open(f'{str(s.file)}', 'rb'))

def download_audio(id):
    w = AudioCreate.objects.get(id=id)
    return FileResponse(open(f'{str(w.audio)}', 'rb'))

def send_notf(from_u, to_u, count):
    from_u = User.objects.get(username=from_u)
    to_u = User.objects.get(username=to_u)
    admin = User.objects.get(username='hello') # Переименуйте на того, кто будет присылать оповещения
    s_1 = f'{to_u} получил ваш подарок, {count} монет!'
    s_2 = f'{from_u} прислал вам подарок, {count} монет!'
    Message.objects.create(user=from_u, sender=admin, reciepient=from_u, body=s_1)
    Message.objects.create(user=to_u, sender=admin, reciepient=to_u, body=s_2)


def send_code(username, phone):
    code = random.randint(1000, 9999)
    phone = f'7{phone[1:]}'
    print(phone)
    sms.sendSMS(phone, f'Ваш код для подтверждения телефона: {code}')
    PhoneCodes.objects.create(username=username, phone=phone, code=code)

def check_code_phone(username, code, request):
    res = PhoneCodes.objects.get(code=code)
    u = User.objects.get(username=username)
    if str(username) == str(res.username) and res.status == False:
        res.status = True
        u.is_verified = True
        res.save()
        u.save()
        return redirect('/create')
    else:
        return render(request, 'video_hosting/smsphone.html', context={'bad': True})

def change_phone(username, phone):
    u = User.objects.get(username=username)
    u.phone = f'7{phone[1:]}'
    u.save()
    send_code(username, phone)

def add_music(audio_path, video_path):
    try:
        video_clip = VideoFileClip(f'{BASE_DIR}/media/{video_path}')
        audio_clip = AudioFileClip(f'{BASE_DIR}/media/{audio_path}')
        video_clip = video_clip.volumex(0.001)
        end = video_clip.duration
        audio = audio_clip.duration
        if audio > end:
            audio_clip = audio_clip.subclip(0, end)
            audio_clip = audio_clip.fx(afx.audio_fadein, 0)
            audio_clip = audio_clip.fx(afx.audio_fadeout, 3)
            final_clip = video_clip.set_audio(audio_clip)
            new_name = str(video_path).split('video1/')
            old_name = new_name[1]
            new_name = old_name.split('.')
            new_name = f'_{new_name[0]}.{new_name[1]}'
            if video_clip.size == [1920,1080]:
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="20000k", threads=20, codec="libx264")
                
            elif video_clip.size == [3840,2160]:
                final_clip = final_clip.resize((1920,1080))
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="20000k", threads=20, codec="libx264")
                
            elif video_clip.size == [2160,3840]:
                final_clip = final_clip.resize((1080,1920))
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="20000k", threads=20, codec="libx264")
                
            else:
                final_clip = final_clip.resize((1080,1920))
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="20000k", threads=20, codec="libx264")
                
            change_video(old_name)    
            
        else: 
            audio_clip = audio_clip.subclip(0, audio)
            audio_clip = audio_clip.fx(afx.audio_fadein, 0)
            audio_clip = audio_clip.fx(afx.audio_fadeout, 3)
            final_clip = video_clip.set_audio(audio_clip)
            new_name = str(video_path).split('video1/')
            old_name = new_name[1]
            new_name = old_name.split('.')
            new_name = f'_{new_name[0]}.{new_name[1]}'
            if video_clip.size == [1920,1080]:
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="20000k", threads=20, codec="libx264")
               
            elif video_clip.size == [3840,2160]:
                final_clip = final_clip.resize((1920,1080))
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="20000k", threads=20, codec="libx264")
                
            elif video_clip.size == [2160,3840]:
                final_clip = final_clip.resize((1080,1920))
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="20000k", threads=20, codec="libx264")
                
            else:
                final_clip = final_clip.resize((1080,1920))
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="20000k", threads=20, codec="libx264")
            change_video(old_name)   
        video_clip.close()
        del_video(old_name)
        
    except:
        return redirect('/createmusic') 
    
       
def change_video(old_name):
    video_obj = VideoCreate.objects.get(file=f'video1/{old_name}')
    video_obj.file = f'video1/_{old_name}'
    a = video_obj.create_at
    #os.remove(f'{BASE_DIR}/media/video1/{old_name}')
    video_obj.name = f'{old_name}'
    video_obj.expiration_date = a
    video_obj.render = True
    video_obj.save()
    
def change_video1(ai, audio_path, video_path1):
    video_obj = ReelsCreate.objects.get(file=audio_path)
    video_obj.file = f'{video_path1}/{ai}'
    video_obj.name = f'_{ai}'
    print(str(video_obj))
    #os.remove(f'{BASE_DIR}/media/video1/{old_name}')
    video_obj.render = True
    video_obj.save()


def change_reels(uid, video_path):
    video_obj = ReelsCreate.objects.create(file=video_path)
    video_obj.file = f'{BASE_DIR}/media/{uid}'
    
    print(str(video_obj))
    
def change_audio(old_name, new_name1, audio_path):
    video_obj = AudioCreate.objects.get(audio=audio_path)
    print(str(video_obj))
    video_obj.audio = f'{BASE_DIR}/media/audio/{new_name1}/_{old_name}'
    video_obj.name = old_name
    #os.remove(f'{BASE_DIR}/media/video1/{old_name}')
    video_obj.render = True
    video_obj.save()
    return redirect('/audiocut')

def change_images(video_path, directory, count):
    
    video_obj = ImagesCreate.objects.get(file=video_path)
    video_obj.file = f'{directory}/{count}.zip'
    #os.remove(f'{BASE_DIR}/media/video1/{old_name}')
    video_obj.name = count
    video_obj.render = True
    video_obj.save()

def change_blackwhite(old_name, new_name1, video_path):
    video_obj = BwCreate.objects.get(file=video_path)
    video_obj.file = f'{BASE_DIR}/media/blackwhite/{new_name1}/_{old_name}'
    video_obj.name = f'{old_name}'
    print(str(video_obj))
    #os.remove(f'{BASE_DIR}/media/video1/{old_name}')
    video_obj.render = True
    video_obj.save()
    change_slowing
    
def change_slowing(old_name, new_name1, video_path):
    video_obj = SlowingCreate.objects.get(file=video_path)
    video_obj.file = f'{BASE_DIR}/media/slowing/{new_name1}/_{old_name}'
    video_obj.name = f'{old_name}'
    print(str(video_obj))
    #os.remove(f'{BASE_DIR}/media/video1/{old_name}')
    video_obj.render = True
    video_obj.save()
    
def change_speed(old_name, new_name1, video_path):
    video_obj = SpeedCreate.objects.get(file=video_path)
    video_obj.file = f'{BASE_DIR}/media/speed/{new_name1}/_{old_name}'
    video_obj.name = f'{old_name}'
    print(str(video_obj))
    #os.remove(f'{BASE_DIR}/media/video1/{old_name}')
    video_obj.render = True
    video_obj.save()
    
def change_render1(old_name, new_name1, video_path):
    video_obj = RenderCreate.objects.get(file=video_path)
    video_obj.file = f'{BASE_DIR}/media/render/{new_name1}/_{old_name}.mp4'
    video_obj.name = f'{old_name}'
    print(str(video_obj))
    #os.remove(f'{BASE_DIR}/media/video1/{old_name}')
    video_obj.render = True
    video_obj.save()
    
def change_render2(old_name, new_name1, video_path):
    video_obj = RendCreate.objects.get(file=video_path)
    video_obj.file = f'{BASE_DIR}/media/render1/{new_name1}/_{old_name}.mp4'
    video_obj.name = f'{old_name}'
    print(str(video_obj))
    #os.remove(f'{BASE_DIR}/media/video1/{old_name}')
    video_obj.render = True
    video_obj.save()

def change_slideshow(video_path):
    video_obj = Slideshow.objects.get(file=video_path)
    video_obj.file = f'{video_path}'
    video_obj.name = f'{video_path}'
    print(str(video_obj))
    #os.remove(f'{BASE_DIR}/media/video1/{old_name}')
    video_obj.render = True
    video_obj.save()
    
def change_videoshow(video_path, count):
    video_obj = Videoshow.objects.get(file=video_path)
    
    video_obj.file = f'{BASE_DIR}/media/videoshow/{count}/zoomin.mp4'
    video_obj.name = f'{video_path}'
    print(str(video_obj))
    #os.remove(f'{BASE_DIR}/media/video1/{old_name}')
    video_obj.render = True
    video_obj.save()     
    
def del_video(old_name):
    time.sleep(10)
    os.remove(f'{BASE_DIR}/media/video1/{old_name}')



def audio_dec(function_to_decorate):
    def wrap(self, form):
        try:
            resp = function_to_decorate(self, form)
        except:
            return None
        if self.object.audio:
            audio_change_back_proc(self.object.audio, self.object.file)
            # add_music(self.object.audio, self.object.file)
        return resp

    return wrap
    

venv = '/home/django/django_venv/bin/python'


def audio_change_back_proc(audio_path, video_path, start_path):
    venv_python = venv
    #venv_python = '/home/django/django_venv/bin/python'
    # venv_python = 'C:/Users/Art/venv/Scripts/python.exe'
    file_path = os.path.join(BASE_DIR, 'video_hosting/audio_back_proc.py')
    subprocess.Popen([venv_python, str(file_path), str(audio_path), str(video_path), str(start_path)])
    

def audio_cut(audio_path, start_path, finish_path):
    venv_python = venv
    # venv_python = 'C:/Users/Art/venv/Scripts/python.exe'
    file_path = os.path.join(BASE_DIR, 'video_hosting/audio_cut.py')
    subprocess.Popen([venv_python, str(file_path), str(audio_path), str(start_path), str(finish_path)])
    
def video_back_proc(audio_path, video_path):
    venv_python = venv
    # venv_python = 'C:/Users/Art/venv/Scripts/python.exe'
    file_path = os.path.join(BASE_DIR, 'video_hosting/video_back_proc.py')
    subprocess.Popen([venv_python, str(file_path), str(audio_path), str(video_path)])
    

def images_back_proc(video_path):
    venv_python = venv
    # venv_python = 'C:/Users/Art/venv/Scripts/python.exe'
    file_path = os.path.join(BASE_DIR, 'video_hosting/images_back_proc.py')
    subprocess.Popen([venv_python, str(file_path), str(video_path)])
    
def blackwhite_back_proc(video_path):
    venv_python = venv
    # venv_python = 'C:/Users/Art/venv/Scripts/python.exe'
    file_path = os.path.join(BASE_DIR, 'video_hosting/blackwhite_back_proc.py')
    subprocess.Popen([venv_python, str(file_path), str(video_path)])


def slowing_back_proc(video_path):
    venv_python = venv
    # venv_python = 'C:/Users/Art/venv/Scripts/python.exe'
    file_path = os.path.join(BASE_DIR, 'video_hosting/slowing_back_proc.py')
    subprocess.Popen([venv_python, str(file_path), str(video_path)])
    
def speed_back_proc(video_path):
    venv_python = venv
    # venv_python = 'C:/Users/Art/venv/Scripts/python.exe'
    file_path = os.path.join(BASE_DIR, 'video_hosting/speed_back_proc.py')
    subprocess.Popen([venv_python, str(file_path), str(video_path)])

def render_back_proc(video_path):
    venv_python = venv
    # venv_python = 'C:/Users/Art/venv/Scripts/python.exe'
    file_path = os.path.join(BASE_DIR, 'video_hosting/render_back_proc.py')
    subprocess.Popen([venv_python, str(file_path), str(video_path)])
    
def render1(video_path):
    venv_python = venv
    # venv_python = 'C:/Users/Art/venv/Scripts/python.exe'
    file_path = os.path.join(BASE_DIR, 'video_hosting/render.py')
    subprocess.Popen([venv_python, str(file_path), str(video_path)])
    
    
def sladeshow(video_path, user, name):
    venv_python = venv
    # venv_python = 'C:/Users/Art/venv/Scripts/python.exe'
    file_path = os.path.join(BASE_DIR, 'video_hosting/sladeshow.py')
    subprocess.Popen([venv_python, str(file_path), str(video_path), str(user), str(name)])
    
def videoshow(video_path, user, name):
    venv_python = venv
    # venv_python = 'C:/Users/Art/venv/Scripts/python.exe'
    file_path = os.path.join(BASE_DIR, 'video_hosting/videoshow.py')
    subprocess.Popen([venv_python, str(file_path), str(video_path), str(user), str(name)])
    
def videoshow1(video_path, user, name):
    venv_python = venv
    # venv_python = 'C:/Users/Art/venv/Scripts/python.exe'
    file_path = os.path.join(BASE_DIR, 'video_hosting/videoshow.py')
    subprocess.Popen([venv_python, str(file_path), str(video_path), str(user), str(name)])
    
#   def video_quality(video_path): # sudo apt-get install ffmpeg
#        file_path = f'{BASE_DIR}/media/{video_path}'
#        cmd = 'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,bit_rate -of default=noprint_wrappers=1 "{}"'.format(file_path)
#        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        
        
#        width, height = None, None
        
#        for line in output.split('\n'):
#            if 'width' in line:
#                width = int(line.split('=')[1])
#            elif 'height' in line:
#                height = int(line.split('=')[1])
            
            
    
 #       if height > 1080 or width > 1920:
            
#            os.rename(file_path, f'{BASE_DIR}/media/video/видео2222332.mp4')
##            cmd = 'ffmpeg -y -i "{}" -vf scale=-1:1080 -c:a copy "{}"'.format(f'{BASE_DIR}/media/video/видео2222332.mp4', file_path)
#            subprocess.call(cmd, shell=True)
#            os.remove(f'{BASE_DIR}/media/video/видео2222332.mp4')
        
        
    
#        return None