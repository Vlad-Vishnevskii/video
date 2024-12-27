from django import forms
from django.forms import Textarea
from .models import Video, VideoCreate, Comments, User, Profile, AudioCreate, ReelsCreate, ImagesCreate, BwCreate, SlowingCreate, RenderCreate, RendCreate, SlideshowCreate, VideoshowCreate, SpeedCreate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
"""
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('file',)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
 """           
 
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
 
class ArticleForm(forms.ModelForm):
    files = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = Video
        fields = ('file', )
    
class ArticleForm1(forms.ModelForm):
    class Meta:
        model = VideoCreate
        fields = ('file', 'audio', 'start')
        required = True
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['id'] = f'id_{field}'
            

class ArticleForm2(forms.Form):
    audio = forms.CharField(max_length=256, label="", required=True, widget=forms.FileInput(attrs={'class': 'form-control','placeholder': 'файл',}))
    start = forms.IntegerField(label="", required=True, widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': 'С какой секунды', 'required': True}))
    finish = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': 'по какую',})) 
     
            
class ArticleForm3(forms.ModelForm):
    class Meta:
        model = ReelsCreate
        fields = ('file', 'audio')
        
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['id'] = f'id_{field}'
            
class ArticleForm4(forms.ModelForm):
    class Meta:
        model = ImagesCreate
        fields = ('file',)
        
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['id'] = f'id_{field}'
            
class ArticleForm5(forms.ModelForm):
    class Meta:
        model = BwCreate
        fields = ('file',)
        
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['id'] = f'id_{field}'

class ArticleForm6(forms.ModelForm):
    class Meta:
        model = SlowingCreate
        fields = ('file',)
        
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['id'] = f'id_{field}'
            
class ArticleForm7(forms.ModelForm):
    class Meta:
        model = RenderCreate
        fields = ('file',)
        
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['id'] = f'id_{field}'
            
class ArticleForm8(forms.ModelForm):
    class Meta:
        model = RendCreate
        fields = ('file',)
        
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['id'] = f'id_{field}'
            
class ArticleForm9(forms.ModelForm):
    files = MultipleFileField(label='Добавьте файлы', required=False)

    class Meta:
        model = SlideshowCreate
        fields = ()
        
class ArticleForm10(forms.ModelForm):
    files = MultipleFileField(label='Добавьте файлы', required=False)

    class Meta:
        model = VideoshowCreate
        fields = ()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['id'] = f'id_{field}'
        
        
class ArticleForm11(forms.ModelForm):
    class Meta:
        model = SpeedCreate
        fields = ('file',)
        
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['id'] = f'id_{field}'
            
class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.input_text = "change"




class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Придумайте пароль'}))
    class Meta:
        model = User
        fields = ['username', 'password', 'birdday', 'gender']
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
        return user
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget = Textarea(attrs={'rows':5}) 
        
        
class EditeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'gender', 'birdday']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
