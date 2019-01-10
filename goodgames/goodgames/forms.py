from django import forms
from django.forms import ModelForm
from goodgames.models import Review


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea, max_length=10000)
    image = forms.FileField(label='Select A File', required=False)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50)


class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, max_length=5000)
    image = forms.FileField(label='Select A File', required=False)


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'body', 'score']
