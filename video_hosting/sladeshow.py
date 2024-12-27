import os
import sys

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
from video_hosting.backends import change_slideshow
from video_hosting.models import Slideshow, User


parameters = sys.argv[1:]

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
count = random.randint(1,10000)


@shared_task         
def rezka(video_path, user, name):
    print(video_path)
    print(f'{name}что за хуйня?')
    images = [f"{video_path}/{img}" for img in sorted(os.listdir(video_path)) if
              img.endswith(('.png', '.jpg', '.jpeg'))]
    directory = f'{video_path}'
    d = (len(images))
    s = os.mkdir(f'{BASE_DIR}/media/skideshow/{count}')
    a = os.getcwd()
    print(a)
    os.chdir(directory)
    a = os.getcwd()
    print(a)
    files_in_dir = [f for f in os.listdir(video_path) if os.path.isfile(f)]
    for i in files_in_dir:
        if i.endswith(('.mp4', '.MP4', '.mov', '.MOV')):
            os.remove(f'{video_path}/{i}')
        else:
        
            m = f'{video_path}/{i}'
            shutil.copy2(f'{m}', f'{BASE_DIR}/media/skideshow/{count}')
            print(m)
    print(files_in_dir)
    #shutil.copy2(f'{files_in_dir}', f'{BASE_DIR}/media/skideshow/{count}')
    files = os.listdir(f'{BASE_DIR}/media/skideshow/{count}')
    print(files)
    os.chdir(f'{BASE_DIR}/media/skideshow/{count}')
    """shutil.copy2(f'{video_path}', f'D:/src06_07_24/media/skideshow/{count}')
    """
    audio = list(filter(lambda x: x.endswith('.mp3') or x.endswith('.MP3') or x.endswith('.wav') or x.endswith('.WAV') or x.endswith('.mpeg'), files))
    clips = []
    print(BASE_DIR)
    for g in random.sample(images, d):
        clips.append(g)
    slides = []
    try:
    
        for n, url in enumerate(clips):
            slides.append(
                mp.ImageClip(url).set_fps(25).set_duration(3).resize(size)
            )

            slides[n] = zoom_in_effect(slides[n], 0.04)
            
        video = mp.concatenate_videoclips(slides)
       
        end = video.duration
        video = video.fx(vfx.fadeout, 2)
        if len(audio) > 0:
            audioclips = [AudioFileClip(c).subclip(0,end) for c in random.sample(audio, 1)]
            ais = concatenate_audioclips(audioclips)
            ais = ais.fx(afx.audio_fadein, 0)
            ais = ais.fx(afx.audio_fadeout, 3)
            video = video.set_audio(ais)
                                        #f'{BASE_DIR}/media/skideshow/{count}/zoomin.mp4'
            video.write_videofile(f'{BASE_DIR}/media/skideshow/{count}/zoomin.mp4')
            ais.close()  
            audioclips[0].close()
        else:
            
            video.write_videofile(f'{BASE_DIR}/media/skideshow/{count}/zoomin.mp4')
        video.close()
        #ais.close()  
        
        #audioclips[0].close()
        dirs = f'{BASE_DIR}/media/skideshow/{count}'
        os.chdir(dirs)
        files1 = os.listdir(dirs)
        #print(files1) 
        a = os.getcwd()
        print(f'{a}фывфыв')
        user = User.objects.get(username=user)
        create = Slideshow(file=f'{BASE_DIR}/media/skideshow/{count}/zoomin.mp4', authors9=user)
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
        print(audio)
        namefile = str(audio[0])
        video_path1 = f'{name}/{namefile}'
        print(video_path1)
        finish = str(video_path1).split('/')[3]
        finish2 = str(video_path1).split('/')[2]
        video_path_ = f'{video_path}/{count}/zoomin.mp4'
        print(f'{finish2}/{finish}/{namefile}')
        change_slideshow(f'{BASE_DIR}/media/skideshow/{count}/zoomin.mp4')
        for li in audio:
            if li != f'zoomin.mp4':
            
        
                os.remove(f'{dirs}/{li}')
        main = name
        os.chdir(main)
        files3 = os.listdir(main)
        audio1 = list(filter(lambda x: x.endswith('.mp3') 
        or x.endswith('.MP3') 
        or x.endswith('.wav') 
        or x.endswith('.WAV') 
        or x.endswith('.mpeg') 
        or x.endswith('.jpeg') 
        or x.endswith('.mp4')
        or x.endswith('.jpg')
        or x.endswith('.png'),files3))
        for si in audio1:
            os.remove(f'{name}/{si}')
        
    except:
        dirs = f'{BASE_DIR}/media/skideshow/{count}'
        os.chdir(dirs)
        files1 = os.listdir(dirs)
        #print(files1) 
        a = os.getcwd()
        
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
        print(audio)
        namefile = str(audio[0])
        video_path1 = f'{name}/{namefile}'
        print(video_path1)
        finish = str(video_path1).split('/')[3]
        finish2 = str(video_path1).split('/')[2]
        print(f'{finish2}/{finish}/{namefile}')
        change_slideshow(f'{BASE_DIR}/media/skideshow/{count}/zoomin.mp4')
        for li in audio:
            if li != f'zoomin.mp4':
                os.remove(f'{dirs}/{li}')
        main1 = name
        os.chdir(main1)
        files4 = os.listdir(main)
        audio2 = list(filter(lambda x: x.endswith('.mp3') 
        or x.endswith('.MP3') 
        or x.endswith('.wav') 
        or x.endswith('.WAV') 
        or x.endswith('.mpeg') 
        or x.endswith('.jpeg') 
        or x.endswith('.mp4')
        or x.endswith('.jpg')
        or x.endswith('.png'),files4))
        
        for di in audio2:
            os.remove(f'{name}/{di}')
    """
      video_obj = SlideshowCreate.objects.get(file=name)
    print(video_obj)
    video_obj.file = f'{name}'
    print(video_obj.file)
    print(str(video_obj))
    #os.remove(f'{BASE_DIR}/media/video1/{old_name}')
    video_obj.render = True
    video_obj.save()
    files = os.listdir(directory)
    print(files)
    counter = count
    print(counter)
    print(video_path)
    change_slideshow(f'{BASE_DIR}/media/skideshow/{count}/zoomin.mp4', f'{counter}', video_path=name)
    """


   
        


print(parameters)
rezka(parameters[0], parameters[1], parameters[2])