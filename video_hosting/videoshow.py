import os
import sys
import time
from celery import shared_task
import django
from django.conf import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR1 = ('C:/Users/Art/appdata/local/programs/python/python310/lib/site-packages')
print(BASE_DIR)
sys.path.append(BASE_DIR)
sys.path.append(BASE_DIR1)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

import math
from PIL import Image
import numpy
import moviepy.editor as mp
from moviepy.editor import *
import random
import shutil
from video_hosting.backends import change_videoshow, videoshow
from video_hosting.models import Videoshow, User


parameters = sys.argv[1:]
"""
count = random.randint(1,1000)
@shared_task 
def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)

        result = numpy.array(img)
        img.close()

        return result

    return clip.fl(effect)
    

size = (1080, 1920)
"""    
count = random.randint(1,1000)


@shared_task         
def rezka(video_path, user, name):
    print(video_path)
    print(f'{name}что за хуйня?')
    images = [f"{video_path}/{img}" for img in sorted(os.listdir(video_path)) if
              img.endswith(('.png', '.jpg', '.jpeg', '.mov', '.mp4', '.MOV', '.MP4'))]
    directory = f'{video_path}'
    d = (len(images))
    s = os.mkdir(f'{BASE_DIR}/media/videoshow/{count}')
    a = os.getcwd()
    print(a)
    os.chdir(directory)
    a = os.getcwd()
    print(a)
    files_in_dir = [f for f in os.listdir(video_path) if os.path.isfile(f)]
    for i in files_in_dir:
        if i.endswith(('.jpg', '.png', '.jpeg')):
            os.remove(f'{video_path}/{i}')
        else:
        
            m = f'{video_path}/{i}'
            shutil.copy2(f'{m}', f'{BASE_DIR}/media/videoshow/{count}')
            print(m)
    print(files_in_dir)
    #shutil.copy2(f'{files_in_dir}', f'{BASE_DIR}/media/skideshow/{count}')
    files = os.listdir(f'{BASE_DIR}/media/videoshow/{count}')
    print(files)
    os.chdir(f'{BASE_DIR}/media/videoshow/{count}')
    """shutil.copy2(f'{video_path}', f'D:/src06_07_24/media/skideshow/{count}')
    """
    audio = list(filter(lambda x: x.endswith('.mp3') or x.endswith('.MP3') or x.endswith('.wav') or x.endswith('.WAV') or x.endswith('.mpeg'), files))
    clips = []
    print(BASE_DIR)
    for g in random.sample(images, d):
        clips.append(g)
    slides = []
    for n, url in enumerate(clips):
        slides.append(
            VideoFileClip(url)
        )

        
        
    video = concatenate_videoclips(slides)
    
      
    video = video.fx(vfx.fadeout, 2)
    size = video.size
    print(size)
   
    end = video.duration
    if len(audio) > 0:
        audioclips = [AudioFileClip(c).subclip(0,end) for c in random.sample(audio, 1)]
        ais = concatenate_audioclips(audioclips)
        ais = ais.fx(afx.audio_fadein, 0)
        ais = ais.fx(afx.audio_fadeout, 3)
        video = video.set_audio(ais)
                                    #f'{BASE_DIR}/media/skideshow/{count}/zoomin.mp4'
        video.write_videofile(f'{BASE_DIR}/media/videoshow/{count}/zoomin.mp4')
        ais.close()  
        audioclips[0].close()
        video.close()
    else:
        
        video.write_videofile(f'{BASE_DIR}/media/videoshow/{count}/zoomin.mp4')
        video.close()
        
    video.close()
    #ais.close()  
    
    #audioclips[0].close()
    dirs = f'{name}'
    os.chdir(dirs)
    files1 = os.listdir(dirs)
    #print(files1) 
    a = os.getcwd()
    print(f'{a}фывфыв')
    user = User.objects.get(username=user)
    create = Videoshow(file=f'{name}/{count}/zoomin.mp4', authors11=user)
    create.save()
    createfile = create.file
    print(user)
    print(files1)
    print(name)
    w = str(files[0])
    namenew = f'{name}{w}'
    print(namenew)
    counter = count
    print(dirs)
    files2 = os.listdir(dirs)
    audio = list(filter(lambda x: x.endswith('.mp3') 
    or x.endswith('.MP3') 
    or x.endswith('.wav') 
    or x.endswith('.WAV') 
    or x.endswith('.mpeg') 
    or x.endswith('.jpeg') 
    or x.endswith('.mp4')
    or x.endswith('.jpg')
    or x.endswith('.png'),files2))
    namefile = str(audio[0])
    video_path1 = f'{name}/{namefile}'
    print(video_path1)
    print(f'{createfile}фывфыв')
    finish = str(video_path1).split('/')[3]
    finish2 = str(video_path1).split('/')[2]
    video_path = f'{createfile}'
    print(f'{finish2}/{finish}/{namefile}')
    change_videoshow(video_path, count)
    time.sleep(10)
    os.chdir(name)
    for li in audio:
    
        os.remove(f'{name}/{li}')
  

    dirs = f'{BASE_DIR}/media/videoshow/{count}'
    files2 = os.listdir(dirs)
    audio1 = list(filter(lambda x: x.endswith('.mp3') 
    or x.endswith('.MP3') 
    or x.endswith('.wav') 
    or x.endswith('.WAV') 
    or x.endswith('.mpeg') 
    or x.endswith('.jpeg') 
    or x.endswith('.mp4')
    or x.endswith('.jpg')
    or x.endswith('.png'),files2))
    for li in audio1:
            if li != f'zoomin.mp4':
                os.remove(f'{dirs}/{li}')    


print(parameters)
rezka(parameters[0], parameters[1], parameters[2])