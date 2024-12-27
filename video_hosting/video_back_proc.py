import os
import sys

from celery import shared_task
import django
from django.conf import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR1 = ('/home/django/django_venv/lib/python3.8/site-packages')
print(BASE_DIR)
sys.path.append(BASE_DIR)
sys.path.append(BASE_DIR1)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from django.shortcuts import redirect
from moviepy.editor import *
from django_project.settings import BASE_DIR
from video_hosting.backends import change_video1, change_reels
import random
import base64
import numpy as np
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import librosa
from scipy.signal import find_peaks
from moviepy.editor import VideoFileClip
import matplotlib.cm as mcm
from tinytag import TinyTag
from moviepy.editor import *
from math import sqrt, sin, cos
import random
import shutil
parameters = sys.argv[1:]

count = random.randint(1,1000)


@shared_task         
def rezka(video_path, audio_path):
    count = str(random.randint(1,10000))
    print(video_path)
    falsse = str(audio_path.split('/')[3])
    uid = str(video_path.split('/')[0])
    print(uid)
    a = os.getcwd()
    p = os.chdir(f'{a}/media/')
   
    if os.path.isdir(f'{uid}'):
        os.mkdir(f'{uid}/{count}')
        a = os.getcwd()
        shutil.copy2(f'{video_path}', f'{uid}/{count}')
        shutil.copy2(f'{audio_path}', f'{uid}/{count}')
        uid1 = str(video_path.split('/')[1])
        uid2 = f'{uid}/{uid1}'
        uid3 = str(audio_path.split('/')[2])
        uid4 = f'{uid}/{uid1}'
        uid5 = (f'{uid}/{uid1}/{uid3}')
        uid6 = f'{uid}/{count}'
        print(uid6 + 'asdad')
        
        uidaudio = str(video_path.split('/')[3])
        vidao = str(audio_path.split('/')[3])
        audio_clip = AudioFileClip(f'{BASE_DIR}/media/{uid6}/{uidaudio}')
        audio_clip.write_audiofile((f'{BASE_DIR}/media/{uid6}/_{uidaudio}'), codec=None)
        print(str(audio_clip))
        print(str(vidao))
        vid = str(vidao.split('.')[0])
        video_clip = VideoFileClip(f'{BASE_DIR}/media/{uid6}/{vidao}')
        video_clip = video_clip.resize((1080, 1920))
        video_clip.write_videofile(f'{BASE_DIR}/media/{uid6}/_{vid}.mp4', bitrate="10000k", threads=2,
                                        codec="libx264")
        video_clip.close()
        os.remove(f'{BASE_DIR}/media/{uid6}/{vidao}')
        y, sr = librosa.load(f'{BASE_DIR}/media/{uid6}/_{uidaudio}')
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

        beat_times = librosa.frames_to_time(beats, sr=sr)
            
        with open(f'{BASE_DIR}/media/{uid6}/start.txt', "w") as file:
            for beat_time in beat_times[0::9]:
                file.write(str(beat_time) + '\n')
                   
                   
        with open(f'{BASE_DIR}/media/{uid6}/start.txt', 'r') as file:
            data = [float(line.strip()) for line in file]
            file.close()
        result = []

        for i in range(len(data)-1):
            result.append(f"{data[i]}-{data[i+1]}")
                

        print(result)

        with open(f'{BASE_DIR}/media/{uid6}/times.txt', 'w') as result_file:
            result_file.write('\n'.join(result))
            result_file.close()
        
        print(audio_path)
        directory = str(f'{BASE_DIR}/media/{uid6}')
        print(directory)
        d = os.getcwd()
        print(d)
        os.chdir(directory)
        f = os.getcwd()
        print(f)
        files = os.listdir(directory)
        print(files)
        video = list(filter(lambda x: x.endswith('.mp4'), files))
        try:
            for m in video:
                count = 0
                video = os.path.join(directory, m)
                print(video)
                with open(f'{BASE_DIR}/media/{uid6}/times.txt') as f:
                                        
                                        
                    times = f.readlines()

                    times = [x.strip() for x in times] 
                    
                                    
                    for time in times:
                        print(m)                  
                        count += 1
                        starttime = float(time.split("-")[0])
                        endtime = float(time.split("-")[1])
                        ffmpeg_extract_subclip(video, starttime, endtime, targetname=str(str(count) + m))
                    f.close()
        except:
            pass
    directory = str(f'{BASE_DIR}/media/{uid6}')
    print(directory)
    d = os.getcwd()
    print(d)
    os.chdir(directory)
    f = os.getcwd()
    print(f)
    files = os.listdir(directory)                
    video1 = list(filter(lambda x: x.endswith('.mp4'), files))                
    aid = str(f'_{vid}.mp4')
    video1.remove(aid) 
         
        
    
    
    new_name1 = f'{uid}/{count}'
    print(new_name1)
    old_name = f'{falsse}'
    
    for d in video1:
        if d.endswith('.mp4'):
            video = TinyTag.get(d)
            if video.duration < 4:
                os.remove(d)

     
            
    
    print(old_name)
    di = str(old_name.split('.')[0])
    video_path1 = uid6
    print(video_path1)
    print(audio_path)
    directory = str(f'{BASE_DIR}/media/{uid6}')
    print(directory)
    d = os.getcwd()
    print(d)
    os.chdir(directory)
    f = os.getcwd()
    print(f)
    files = os.listdir(directory)
    print(files)
    video = list(filter(lambda x: x.endswith('.mp4'), files))
    audio = list(filter(lambda x: x.endswith('.mp3'), files))
    aid = str(f'_{vid}.mp4')
    ai = str(f'{vid}.mp4')
    video.remove(aid)
    for m in video:
           # video_clips = [VideoFileClip(m).subclip(0,3).subfx(lambda c:c.speedx(0.5) , 1,3).resize(lambda swelling: 1.3 + 0.3 * sin(swelling / 3)) for m in random.sample(video, 2)]
        count += 1
        padding = 1
        video_clips = [VideoFileClip(m).subclip(0,3).subfx(lambda c:c.speedx(0.5) , 1, 3 ) for m in random.sample(video, len(video))]
    
        video_fx_list = [video_clips[0]]
        
        idx = video_clips[0].duration - padding
        for video in video_clips[1:]:
            video_fx_list.append(video.set_start(idx).crossfadein(padding))
            idx += video.duration - padding
        
            final_video = CompositeVideoClip(video_fx_list)
            
        final_clip = final_video.volumex(0.01)
        end = final_clip.duration
        audioclips = [AudioFileClip(c) for c in random.sample(audio, 1)]
        ais = concatenate_audioclips(audioclips)
        p = ais.duration
        
        if p > end:
            final_clip = final_clip.subclip(0, end)
            final_clip = final_clip.fx(vfx.fadeout, 2)
            ais = ais.subclip(0, end)
            ais = ais.fx(afx.audio_fadein, 0)
            ais = ais.fx(afx.audio_fadeout, 3)
            final_clip = final_clip.set_audio(ais)
            final_clip = final_clip.resize((1080,1920))
            final_clip.write_videofile(f'_{ai}',
                                               threads=2, 
                verbose=False,
                logger="bar",
                bitrate="5000k",
                audio_codec="aac",
                codec="libx264",)
            change_video1(aid, audio_path, video_path1)
        else:
            final_clip = final_clip.subclip(0, p)
            final_clip = final_clip.fx(vfx.fadeout, 2)
            ais = ais.subclip(0, p)
            ais = ais.fx(afx.audio_fadein, 0)
            ais = ais.fx(afx.audio_fadeout, 3)
            final_clip = final_clip.set_audio(ais)
            final_clip = final_clip.resize((1080,1920))
            final_clip.write_videofile(f'_{ai}',
                                               threads=2,
                 
                verbose=False,
                logger="bar",
                bitrate="5000k",
                audio_codec="aac",
                codec="libx264",)
                
                
            change_video1(aid, audio_path, video_path1)

        
        
        final_clip.close()
               
   
    

    
                    


    



   
        


print(parameters)
rezka(parameters[0],parameters[1])