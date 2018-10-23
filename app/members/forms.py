from django import forms

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
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exist():
            raise form.ValidationError('이미 사용중인 계정입니다.')
        return data

    def clean(self):
        # password1, password2가 일치하는지 검사
        super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('비밀번호가 같지 않습니다.')

