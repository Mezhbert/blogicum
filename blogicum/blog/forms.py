from django import forms
from .models import Post, User, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'category', 'location', 'pub_date']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
