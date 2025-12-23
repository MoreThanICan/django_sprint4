from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Post, Comment, Category, Location

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'category', 'location', 'image')
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'min': '2000-01-01T00:00',
                    'max': '2099-12-31T23:59'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.pub_date:
                self.initial['pub_date'] = self.instance.pub_date.strftime('%Y-%m-%dT%H:%M')
        self.fields['pub_date'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']
        self.fields['location'].queryset = Location.objects.filter(is_published=True).order_by('name')
        self.fields['location'].empty_label = "Выберите местоположение"


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

