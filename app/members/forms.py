from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 이 Form instance에 주어진 데이터가 유효하면
        # authenticate에서 리턴돈 User객체를 체울 속성
        self._user = None
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

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('틀렸습니다.')
        self._user = user

    @property
    # 유효성 검증을 실행했을 때 (is_valid())
    # 만약 필드나 폼에서 유효하지 않은 항목이 있다면
    # 이 부분에 추가
    def user(self):
        if self.errors:
            raise ValueError('폼의 데이터 유효성 검증에 실패하였습니다.')
        return self._user


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


