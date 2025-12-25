from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
import pytz

from .models import Post, Comment, Category, Location

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'created_at')
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'min': '2000-01-01T00:00',
                    'max': '2099-12-31T23:59'
                }
            ),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'is_published': 'Виден для всех'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.pub_date:
                local_tz = pytz.timezone('Europe/Saratov')
                local_time = self.instance.pub_date.astimezone(local_tz)
                self.initial['pub_date'] = local_time.strftime('%Y-%m-%dT%H:%M')
            self.initial['is_published'] = self.instance.is_published
        self.fields['pub_date'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']
        self.fields['location'].queryset = Location.objects.filter(is_published=True).order_by('name')
        self.fields['location'].empty_label = "Выберите местоположение"
    
    def clean_pub_date(self):
        pub_date = self.cleaned_data.get('pub_date')
        if pub_date:
            local_tz = pytz.timezone('Europe/Saratov')
            if timezone.is_naive(pub_date):
                pub_date = local_tz.localize(pub_date)
            return pub_date
        return pub_date


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

