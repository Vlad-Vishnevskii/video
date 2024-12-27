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
from backends import change_audio

parameters = sys.argv[1:]
@shared_task
def cut_music(audio_path, start_path, finish_path):
    try:
        if audio_path.endswith('.mp3'):
            audio_clip = AudioFileClip(f'{BASE_DIR}/media/{audio_path}')
            uid = str(audio_path.split('/')[2])
            new_clip = audio_clip.subclip(start_path, finish_path)
            new_name = str(audio_path).split('/')
            new_name1 = new_name[1]
            old_name = new_name[2]
            new_name = f'{new_name[0]}.{old_name}'
            new_clip.write_audiofile(f'{BASE_DIR}/media/audio/{new_name1}/_{old_name}', 
            fps=None,
                nbytes=2,
                buffersize=2000,
                bitrate=None,
                ffmpeg_params=None,
                write_logfile=False,
                logger="bar",
            )
            change_audio(old_name, new_name1, audio_path)
            new_clip.close()
        else:
            audio_clip = VideoFileClip(f'{BASE_DIR}/media/{audio_path}')
            uid = str(audio_path.split('/')[2])
            new_clip = audio_clip.subclip(start_path, finish_path)
            new_name = str(audio_path).split('/')
            new_name1 = new_name[1]
            old_name = new_name[2]
            new_clip.write_videofile(f'{BASE_DIR}/media/audio/{new_name1}/_{old_name}',
                                                   threads=2,
                    fps=50, 
                    verbose=False,
                    logger="bar",
                    bitrate="5000k",
                    audio_codec="aac",
                    codec="libx264",)
            change_audio(old_name, new_name1, audio_path)
            new_clip.close()
    except:
        audio_clip = AudioFileClip(f'{BASE_DIR}/media/{audio_path}')
        uid = str(audio_path.split('/')[2])
        new_clip = audio_clip.subclip(start_path, finish_path)
        new_name = str(audio_path).split('/')
        new_name1 = new_name[1]
        old_name = new_name[2]
        new_name = f'{new_name[0]}.{old_name}'
        new_clip.write_audiofile(f'{BASE_DIR}/media/audio/{new_name1}/_{old_name}', 
        fps=None,
            nbytes=2,
            buffersize=2000,
            bitrate=None,
            ffmpeg_params=None,
            write_logfile=False,
            logger="bar",
        )
        change_audio(old_name, new_name1, audio_path)
        new_clip.close()
print(parameters)
cut_music(parameters[0], parameters[1], parameters[2])
