from django import forms
# from django.forms import ModelForm
# from goodgames.models import Image


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


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50)


class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, max_length=5000)


# class ImageForm(ModelForm):
#     class Meta:
#         model = Image
