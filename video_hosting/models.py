from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from video_hosting.managers import UserManager
from django.core.validators import RegexValidator
from django.db.models.signals import post_save, post_delete
import uuid
from django.core.files.storage import FileSystemStorage
import time
import random
import datetime
# import PIL
# from PIL import Image
count = 1


class User(AbstractBaseUser, PermissionsMixin):
    GENDER = [
    ('M', 'Мужчина'),
    ('F', 'Женщина'),
    ]
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Имя должно быть на латинице.')
    username = models.CharField(_('username'), max_length=255, unique=True, validators=[alphanumeric])
    email = models.EmailField(_('email address'),\
        null=True, blank=True)
    phone = models.CharField(_('Телефон'), max_length=30,\
        )
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    avatar = models.ImageField(verbose_name = 'Аватар', null=True, blank=True, upload_to="images/profile/")
    bio=models.TextField(verbose_name = 'О себе', null=True, blank=True)
    facebook = models.CharField(max_length=50, null=True, blank=True)
    twitter = models.CharField(max_length=50, null=True, blank=True)
    instagram = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    gender = models.CharField( choices=GENDER, max_length=1, verbose_name='Пол', null=True, blank=True)
    birdday = models.DateField(verbose_name='Дата рождения', null=True, blank=True)


    is_verified = models.BooleanField(_('verified'), default=False)
    start_month = models.DateTimeField(null=True, blank=True)
    finish_month = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def datepublished(self):
        return self.finish_month.strftime('%Y-%m-%d')
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = ('username', 'email', 'phone')
    
    
    
    
class Montaj(models.Model):
    filemod = models.FileField(
        upload_to='video1/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    
class IpModel(models.Model):
    ip = models.CharField(max_length=100)
    
    def __str__(self):
        return self.ip

class Video(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors')
    
    #description = models.TextField(verbose_name = 'Добавить подпись', blank=True)
    image = models.ImageField(verbose_name = 'Обложка',upload_to='image/', blank=True)
    file = models.FileField(verbose_name = 'Видео',
        upload_to='video/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov'])]
    )
    
    create_at = models.DateTimeField(auto_now_add=True)
    
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    views = models.ManyToManyField(IpModel, related_name="post_views", blank=True)
    def __str__(self):
        return self.title
        
    def total_views(self):
        return self.views.count()
        
class VideoCreate(models.Model):
    authors = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creates', null=True)
    
    file = models.FileField(verbose_name = 'Видео',
        upload_to='video1/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'insv'])],
        null=True, blank=True
    )
    audio = models.FileField(verbose_name='Музыка',
        upload_to='video1/',
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])],
        
        null=True, blank=True
    )
    start = models.IntegerField(verbose_name='С какой секунды начинаем', default=0)
    name = models.CharField(max_length=100, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    render = models.BooleanField(default=False)
    
class AudioCreate(models.Model):
    authors1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creates1', null=True)
    p = uuid.uuid4()
    audio = models.FileField(verbose_name='Загрузите песню',
        upload_to=f'audio/{p}',
        validators=[FileExtensionValidator(allowed_extensions=['mp3','mp4'])],
        
        
    )
    start = models.IntegerField(verbose_name='С какой секунды начинаем', blank=False, null=False)
    finish = models.IntegerField(verbose_name='На какой заканчиваем', blank=False, null=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True) 
    render = models.BooleanField(default=False)    


class ReelsCreate(models.Model):
    authors2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reels', null=True)
    a = uuid.uuid4()
    
    id = models.AutoField(primary_key=True)
    random_string = random.randint(10000, 99999)
    file = models.FileField(verbose_name = 'Видео',
        upload_to=f'reels/{a}/{random_string}',
        validators=[FileExtensionValidator(allowed_extensions=['mp3','mp4', 'mov', 'insv'])]
    )
    audio = models.FileField(verbose_name='Музыка',
        upload_to=f'reels/{a}/{random_string}',
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'mp4', 'mov', 'insv'])],
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    render = models.BooleanField(default=False)
    
    
            

    
class ImagesCreate(models.Model):
    authors3 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images', null=True)
    p = uuid.uuid4()
    random_string = random.randint(10000, 99999)
    file = models.FileField(verbose_name = 'Видео',
        upload_to=f'images_zip/{p}/{random_string}',
        validators=[FileExtensionValidator(allowed_extensions=['mp3','mp4', 'mov', 'insv'])]
    )
    create_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    render = models.BooleanField(default=False)
    
class BwCreate(models.Model):
    authors4 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blackwhite', null=True)
    p = uuid.uuid4()
    
    file = models.FileField(verbose_name = 'Видео',
        upload_to=f'blackwhite/{p}',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'insv'])]
    )
    create_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    render = models.BooleanField(default=False)
        
 
class SlowingCreate(models.Model):
    authors5 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slowing', null=True)
    p = uuid.uuid4()
    
    file = models.FileField(verbose_name = 'Видео',
        upload_to=f'slowing/{p}',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'insv'])]
    )
    create_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    render = models.BooleanField(default=False)
    
class SpeedCreate(models.Model):
    authors12 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='speed', null=True)
    p = uuid.uuid4()
    
    file = models.FileField(verbose_name = 'Видео',
        upload_to=f'speed/{p}',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'insv'])]
    )
    create_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    render = models.BooleanField(default=False)

class RenderCreate(models.Model):
    authors6 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='render1', null=True)
    p = uuid.uuid4()
    
    file = models.FileField(verbose_name = 'Видео',
        upload_to=f'render/{p}',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'insv', 'MOV', 'MP4'])]
    )
    create_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    render = models.BooleanField(default=False)


    
class RendCreate(models.Model):
    authors7 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='render2', null=True)
    p = uuid.uuid4()
    
    file = models.FileField(verbose_name = 'Видео',
        upload_to=f'render1/{p}',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'insv', 'MOV', 'MP4'])]
    )
    create_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    render = models.BooleanField(default=False)
    
class SlideshowCreate(models.Model):
    authors8 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slideshow', null=True)
    p = uuid.uuid4()
    file = models.FileField(verbose_name = 'Слайдшоу',
        upload_to=f'skideshow/{p}/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])]
    )
    
    audio = models.FileField(verbose_name='Музыка',
        upload_to=f'skideshow/{p}/',
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])],
        
        null=True, blank=True
    )
    create_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    render = models.BooleanField(default=False)
    
class Slideshow(models.Model):
    authors9 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slideshow1', null=True)
    p = uuid.uuid4()
    file = models.FileField(verbose_name = 'Слайдшоу',
        upload_to=f'skideshow/{p}/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    
    audio = models.FileField(verbose_name='Музыка',
        upload_to=f'skideshow/{p}/',
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])],
        
        null=True, blank=True
    )
    create_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    render = models.BooleanField(default=False)

class VideoshowCreate(models.Model):
    authors10 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videoshow3', null=True)
    p = uuid.uuid4()
    file = models.FileField(verbose_name = 'Слайдшоу',
        upload_to=f'videoshow/{p}/',
    )
    
    audio = models.FileField(verbose_name='Музыка',
        upload_to=f'videoshow/{p}/',
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])],
        
        null=True, blank=True
    )
    create_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    render = models.BooleanField(default=False)
    
class Videoshow(models.Model):
    authors11 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videoshow1', null=True)
    p = uuid.uuid4()
    file = models.FileField(verbose_name = 'Слайдшоу',
        upload_to=f'videoshow/{p}/',
    )
    
    audio = models.FileField(verbose_name='Музыка',
        upload_to=f'videoshow/{p}/',
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])],
        
        null=True, blank=True
    )
    create_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    render = models.BooleanField(default=False)
    
class Comments(models.Model):
    article = models.ForeignKey(Video, on_delete = models.CASCADE, verbose_name = 'Автор', blank = True, null = True, related_name='comments_video')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость статьи', default=False)

class Profile(models.Model):

    GENDER = [
    ('M', 'Мужчина'),
    ('F', 'Женщина'),
    ]
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name = 'Аватар', null=True, blank=True, upload_to="images/profile/")
    gender = models.CharField( choices=GENDER, max_length=1, verbose_name='Пол', null=True, blank=True)
    birdday = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    
   
    def __str__(self):
        return f'{self.user.username} - Profile'
        
class MeetingRequest(models.Model):
    STATUS_CHOICES = [
        ('send', 'Отправлено'),
        ('accepted', 'Принято'),
        ('declined', 'Отклонено'),
    ]

    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='send')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Запрос от {self.from_user.username} к {self.to_user.username} - {self.status}'    


def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):

	instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


class FollowersCount(models.Model):
    user = models.CharField(max_length=100, blank = True, null = True)
    follower = models.CharField(max_length=100, blank = True, null = True)
    
    def __str__(self):
        return self.user

class WalletUser(models.Model):
    user_id = models.IntegerField(null=False)
    condition = models.FloatField(default=0.0, null=False)

class Check(models.Model):
    check_info = models.CharField(max_length=200, null=False)
    status = models.BooleanField(default=False) # Если фолс то юзер еще не вводил данные на сайте
    money = models.IntegerField(null=True)

class Audio(models.Model):
    audio_path = models.CharField(max_length=500, null=False)

