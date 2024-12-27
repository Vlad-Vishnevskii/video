import os
import sys

from celery import shared_task
import django
from django.conf import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from django.shortcuts import redirect
from moviepy.editor import *
import numpy as np
import os
from datetime import timedelta
from zipfile import ZipFile
from video_hosting.backends import change_images
import random
import shutil
parameters = sys.argv[1:]
SAVING_FRAMES_PER_SECOND = 5



def format_timedelta(td):
    result = str(td)
    try:
        result, ms = result.split(".")
    
    except ValueError:
        return result + ".00".replace(":", "-")
        
    ms = round(int(ms) / 10000)
    return f"{result}.{ms:02}".replace(":", "-")



@shared_task  
def main(video_path):
    count = str(random.randint(1,1000))
    video_clip = VideoFileClip(f'{BASE_DIR}/media/{video_path}')
    print(video_path)
    uid = str(video_path.split('/')[0])
    print(uid + 'uid')
    uid1 = str(video_path.split('/')[1])
    print(uid1)
    uid2 = f'{uid}/{uid1}'
    uid3 = str(video_path.split('/')[3])
    filename = f'{BASE_DIR}/media/{uid2}'   
    print(uid2 + ' uid2')
    print(filename)
    a = os.getcwd()
    p = os.chdir(f'{a}/media/')
    print(a + ' sda')
    print(video_path)
    if os.path.isdir(f'{uid2}'):
        os.mkdir(f'{uid2}/{count}')
        a = os.getcwd()
        filename = f'{BASE_DIR}/media/{uid2}/{count}' 
        shutil.copy2(f'{video_path}', f'{uid2}/{count}')
        os.chdir(f'{uid2}/{count}')
        saving_frames_per_second = min(video_clip.fps, SAVING_FRAMES_PER_SECOND)
        step = 1 / video_clip.fps if saving_frames_per_second == 0 else 1 / saving_frames_per_second
        
        for current_duration in np.arange(0, video_clip.duration, step):
            frame_duration_formatted = format_timedelta(timedelta(seconds=current_duration)).replace(":", "-")
            frame_filename = os.path.join(filename, f"frame{frame_duration_formatted}.jpg")
            
            video_clip.save_frame(frame_filename, current_duration)
        
    directory = (f'{BASE_DIR}/media/{uid2}/{count}')   
    files = os.listdir(directory)
    image = list(filter(lambda x: x.endswith('.jpg'), files))
    
    os.chdir(directory)
    a = os.getcwd()
    print(a)
    with ZipFile((f'{count}.zip'), "w") as myzip:
        for i in image:
            myzip.write(i)
            
    change_images(video_path, directory, count)
   


print(parameters)      
        
main(parameters[0])
#image_zip = video_path.split('.')[0]

