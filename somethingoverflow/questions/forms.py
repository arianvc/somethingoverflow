from django import forms
from django.contrib.auth.models import User
from .models import Question, Post


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'})
        }


class RecoverForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    # TODO: captcha
    # TODO: SMS recovery


class ResetForm(forms.Form):  # TODO: use modelform for use with different fields?
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    recovery_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Recovery Code'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password, 8 alphanumeric at least'}))


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'body')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )
