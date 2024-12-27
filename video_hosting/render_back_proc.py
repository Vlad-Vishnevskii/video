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
from backends import change_render1

parameters = sys.argv[1:]
@shared_task
def render_video(video_path):
    new_clip = VideoFileClip(f'{BASE_DIR}/media/{video_path}')
    uid = str(video_path.split('/')[2])
    new_name = str(video_path).split('/')
    new_name1 = new_name[1]
    print(new_name1)
    old_name = new_name[2]
    old_name = str(old_name).split('.')[0]
    print(old_name)
    new_name = f'{new_name[0]}.{old_name}'
    if new_clip.size == [1920,1080]:
        new_clip.write_videofile(f'{BASE_DIR}/media/render/{new_name1}/_{old_name}.mp4')
        change_render1(old_name, new_name1, video_path)
        new_clip.close()
    elif new_clip.size == [3840,2160]:
        new_clip = new_clip.resize((1920,1080))
        new_clip.write_videofile(f'{BASE_DIR}/media/render/{new_name1}/_{old_name}.mp4')
        change_render1(old_name, new_name1, video_path)
        new_clip.close()

    elif new_clip.size == [2160,3840]:
        new_clip = new_clip.resize((1080,1920))
        new_clip.write_videofile(f'{BASE_DIR}/media/render/{new_name1}/_{old_name}.mp4')
        change_render1(old_name, new_name1, video_path)
        new_clip.close()

    else:
        new_clip = new_clip.resize((1080,1920))
        new_clip.write_videofile(f'{BASE_DIR}/media/render/{new_name1}/_{old_name}.mp4')
    
        change_render1(old_name, new_name1, video_path)
        new_clip.close()
    
       
print(parameters)
render_video(parameters[0])
