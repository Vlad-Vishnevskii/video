import os
import sys

from celery import shared_task
import django
from django.conf import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()
"""
final_clip2 = str(final_clip.size).split(',')
                ad = final_clip1[1]
                ad1 = str(ad).split(')')
                ad2 = final_clip2[0]
                ad3 = str(ad2).split('(')
                x = int(ad1[0])
                y = int(ad3[1])
                print(x)
                print(y)
                print(final_clip1)
                print(ad)
"""
from django.shortcuts import redirect
from moviepy.editor import *
from backends import change_video, del_video
import random
parameters = sys.argv[1:]

@shared_task
def add_music(audio_path, video_path, start_path):
    try:
        if audio_path == None:
            print('sada')
        if start_path != None:
            count = str(random.randint(1,10000))
            print(video_path)
            print(audio_path)
            print(start_path)
            video_clip = VideoFileClip(f'{BASE_DIR}/media/{audio_path}')
            audio_clip = AudioFileClip(f'{BASE_DIR}/media/{video_path}')
            i = video_path.split('/')[1]
            audio = audio_clip.duration
            audio_clip = audio_clip.subclip(int(start_path), audio)
            audio_clip.write_audiofile(f'{BASE_DIR}/media/video1/_{i}')
            video_clip = video_clip.volumex(0.001)
            audio1 = AudioFileClip(f'{BASE_DIR}/media/video1/_{i}')
            audio_duration = audio1.duration
            end = video_clip.duration
            print(audio)
            if audio_duration > end:
                audio1 = audio1.subclip(0, end)
                audio1 = audio1.fx(afx.audio_fadein, 0)
                audio1 = audio1.fx(afx.audio_fadeout, 3)
                final_clip = video_clip.set_audio(audio1)
                final_clip = final_clip.fx(vfx.fadeout, 1)
                new_name = str(video_path).split('video1/')
                old_name = new_name[1]
                new_name = old_name.split('.')
                new_name = f'_{new_name[0]}.{new_name[1]}'
                print(new_name)
                if video_clip.size == [1920, 1080]:
                        # final_clip = final_clip.resize((1080, 1920))
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                                   codec="libvpx")

                elif video_clip.size == [3840, 2160]:
                    final_clip = final_clip.resize((1920, 1080))
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                                   codec="libvpx")

                elif video_clip.size == [2160, 3840]:
                    final_clip = final_clip.resize((1080, 1920))
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                                   codec="libvpx")

                else:
                    final_clip == [608, 1080]
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                           codec="libx264")

                change_video(old_name)

            else:
                video_clip = video_clip.subclip(0, audio_duration)
                audio1 = audio1.fx(afx.audio_fadein, 0)
                audio1 = audio1.fx(afx.audio_fadeout, 3)
                final_clip = video_clip.set_audio(audio1)
                final_clip = final_clip.fx(vfx.fadeout, 1)
                new_name = str(audio_path).split('video1/')
                old_name = new_name[1]
                new_name = old_name.split('.')
                new_name = f'_{new_name[0]}.{new_name[1]}'
                print(new_name)
                if video_clip.size == [1920, 1080]:
                        # final_clip = final_clip.resize((1080, 1920))
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                                   codec="libx264")

                elif video_clip.size == [3840, 2160]:
                    final_clip = final_clip.resize((1920, 1080))
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                                   codec="libx264")

                elif video_clip.size == [2160, 3840]:
                    final_clip = final_clip.resize((1080, 1920))
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                                   codec="libx264")

                else:
                    final_clip == [608, 1080]
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                           codec="libx264")

                change_video(old_name)
        else:
            video_clip = VideoFileClip(f'{BASE_DIR}/media/{audio_path}')
            audio_clip = AudioFileClip(f'{BASE_DIR}/media/{video_path}')
            video_clip = video_clip.volumex(0.001)
            end = video_clip.duration
            audio = audio_clip.duration
            print(audio)
            if audio > end:
                audio_clip = audio_clip.subclip(0, end)
                audio_clip = audio_clip.fx(afx.audio_fadein, 0)
                audio_clip = audio_clip.fx(afx.audio_fadeout, 3)
                final_clip = video_clip.set_audio(audio_clip)
                final_clip = final_clip.fx(vfx.fadeout, 1)
                new_name = str(audio_path).split('video1/')
                old_name = new_name[1]
                new_name = old_name.split('.')
                new_name = f'_{new_name[0]}.{new_name[1]}'
                if video_clip.size == [1920, 1080]:
                        # final_clip = final_clip.resize((1080, 1920))
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                                   codec="libx264")

                elif video_clip.size == [3840, 2160]:
                    final_clip = final_clip.resize((1920, 1080))
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                                   codec="libx264")

                elif video_clip.size == [2160, 3840]:
                    final_clip = final_clip.resize((1080, 1920))
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                                   codec="libx264")

                else:
                    final_clip == [608, 1080]
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                           codec="libx264")

                change_video(old_name)

            else:
                loops = end // audio + 1  # Количество повторений аудио
                audio_clips = [audio_clip] * int(loops)  # Создаем список из повторяющихся аудиоклипов
                concatenated_audio = concatenate_audioclips(audio_clips)  # Соединяем аудиоклипы в один
                audio_clip = concatenated_audio.subclip(0, end)  # Обрезаем получившийся аудиоклип до длительности видео
                audio_clip = audio_clip.fx(afx.audio_fadein, 0)
                audio_clip = audio_clip.fx(afx.audio_fadeout, 3)
                final_clip = video_clip.set_audio(audio_clip)
                final_clip = final_clip.fx(vfx.fadeout, 1)                # Заменяем аудиодорожку видео
                new_name = str(video_path).split('video1/')

                old_name = new_name[1]
                new_name = old_name.split('.')
                new_name = f'_{new_name[0]}.{new_name[1]}'
                print(new_name, ' !!!!!!!!!!!!!!')
                if video_clip.size == [1920, 1080]:
                    final_clip = final_clip.resize((1080, 1920))
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                                   codec="libx264")

                elif video_clip.size == [3840, 2160]:
                    final_clip = final_clip.resize((1920, 1080))
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                                   codec="libx264")

                elif video_clip.size == [2160, 3840]:
                    final_clip = final_clip.resize((1080, 1920))
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                                   codec="libx264")

                else:
                    final_clip == [608, 1080]
                    final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                           codec="libx264")
                change_video(old_name)
                video_clip.close()
                #del_video(old_name)
            
    except:
        video_clip = VideoFileClip(f'{BASE_DIR}/media/{audio_path}')
        audio_clip = AudioFileClip(f'{BASE_DIR}/media/video1/_{i}')
        video_clip = video_clip.volumex(0.001)
        end = video_clip.duration
        audio = audio_clip.duration
        if audio > end:
            print('audio больше video')
            audio_clip = audio_clip.subclip(0, end)
            audio_clip = audio_clip.fx(afx.audio_fadein, 0)
            audio_clip = audio_clip.fx(afx.audio_fadeout, 3)
            final_clip = video_clip.set_audio(audio_clip)
            final_clip = final_clip.fx(vfx.fadeout, 1)
            final_clip2 = str(final_clip.size).split(',')
            ad = final_clip2[1]
            ad1 = str(ad).split(')')
            ad2 = final_clip2[0]
            ad3 = str(ad2).split('(')
            x = int(ad1[0])
            y = int(ad3[1])
            print(x)
            print(y)
            print(ad)
            new_name = str(audio_path).split('video1/')
            old_name = new_name[1]
            new_name = old_name.split('.')
            new_name = f'_{new_name[0]}.{new_name[1]}'
            if video_clip.size == [1920, 1080]:
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                           codec="libx264")
            elif video_clip.size == [608, 1080]:
                final_clip = final_clip.resize((1080, 1920))
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                           codec="libx264")
            elif video_clip.size == [3840, 2160]:
                final_clip = final_clip.resize((1920, 1080))
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                           codec="libx264")

            elif video_clip.size == [2160, 3840]:
                final_clip = final_clip.resize((1080, 1920))
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                           codec="libx264")

            else:
                final_clip == [608, 1080]
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                           codec="libx264")

            change_video(old_name)

        else:
            print('audio меньше video')
            audio_clip = audio_clip.subclip(0, audio)
            audio_clip = audio_clip.fx(afx.audio_fadein, 0)
            audio_clip = audio_clip.fx(afx.audio_fadeout, 3)
            final_clip = video_clip.set_audio(audio_clip)
            final_clip = final_clip.fx(vfx.fadeout, 1)
            new_name = str(video_path).split('video1/')
            old_name = new_name[1]
            new_name = old_name.split('.')
            new_name = f'_{new_name[0]}.{new_name[1]}'
            if video_clip.size == [1920, 1080]:
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                           codec="libx264")

            elif video_clip.size == [3840, 2160]:
                final_clip = final_clip.resize((1920, 1080))
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                           codec="libx264")

            elif video_clip.size == [2160, 3840]:
                final_clip = final_clip.resize((1080, 1920))
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                           codec="libx264")

            else:
                final_clip == [1080, 1920]
                final_clip.write_videofile(f'{BASE_DIR}/media/video1/{new_name}', fps=30, bitrate="10000k", threads=2,
                                           codec="libx264")

            change_video(old_name)
        video_clip.close()
        #del_video(old_name)
        return redirect('/createmusic')

print(parameters)
add_music(parameters[0], parameters[1], parameters[2])

