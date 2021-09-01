from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label="아이디 ", help_text="150자 이하의 영문자, 숫자, 특수문자(@, ., +, -, _ 만 가능)를 입력해주세요")
    email = forms.EmailField(label="이메일 ", widget=forms.EmailInput(attrs={'class': 'input email', 'placeholder': 'example@gmail.com'}))
    first_name = forms.CharField(label="성")
    last_name = forms.CharField(label="이름")
    password = forms.CharField(label="비밀번호 ", widget=forms.PasswordInput)
    password2 = forms.CharField(label="비밀번호 재입력 ", widget=forms.PasswordInput)

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('이미 있는 아이디 입니다.')
        return cd['username']

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['email']).exists():
            raise forms.ValidationError('이미 있는 이메일 입니다.')
        return cd['email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호가 다릅니다.')
        return cd['password2']

class LoginForm(forms.Form):
    username = forms.CharField(label="아이디 ")
    password = forms.CharField(label="비밀번호 ", widget=forms.PasswordInput)

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            return cd['username']
        raise forms.ValidationError('존재하지 않는 아이디 입니다.')

    def clean_password(self):
        cd = self.cleaned_data
        _user = User.objects.get(username=cd['username'])
        if check_password(cd['password'], _user.password):
            return cd['password']
        raise forms.ValidationError('일치하지 않는 비밀번호입니다.')