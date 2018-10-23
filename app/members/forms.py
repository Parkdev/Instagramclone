from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        # 일반 input[type=text]
        # form-control CSS클래스 사용
        # (Bootstrap규칙)
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

class SignupForm(forms.Form):
    #폼에 클래스를 추가해서 색을 변경하는등의 작업을 할 수 있다.
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('이미 사용중인 계정입니다.')
        return data

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('비밀번호가 다릅니다.')
        return password2

    # def clean(self):
    #     # password1, password2가 일치하는지 검사
    #     super().clean()
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 != password2:
    #         raise forms.ValidationError('비밀번호가 같지 않습니다.')

    def save(self):
        if self.errors:
            raise ValueError('폼의 데이터 유효성 검증에 실패')
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
        )
        return user