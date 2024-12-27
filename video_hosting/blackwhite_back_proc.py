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
from backends import change_blackwhite

parameters = sys.argv[1:]
@shared_task
def blackwhite(video_path):
    new_clip = VideoFileClip(f'{BASE_DIR}/media/{video_path}')
    new_clip = new_clip.fx(vfx.blackwhite)
    uid = str(video_path.split('/')[2])
    new_name = str(video_path).split('/')
    new_name1 = new_name[1]
    old_name = new_name[2]
    new_name = f'{new_name[0]}.{old_name}'
    new_clip.write_videofile(f'{BASE_DIR}/media/blackwhite/{new_name1}/_{old_name}',
                                                   threads=2,
                    fps=50, 
                    verbose=False,
                    logger="bar",
                    bitrate="5000k",
                    audio_codec="aac",
                    codec="libx264",)
    change_blackwhite(old_name, new_name1, video_path)
    new_clip.close()
       
print(parameters)
blackwhite(parameters[0])
