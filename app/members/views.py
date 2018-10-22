from django.shortcuts import render

# Create your views here.
from members.forms import LoginForm


def login_view(request):
    # URL: /members/login/
    # config.urls에서 '/members/'부분을 "members.urls'를 사용하도록 include
    # members.urls에서 '/login/' 부분을 이 view에 연결

    # Template: members/login.html
    # 템플릿에는 아래의 LoginForm인스턴스를 사용

    # Form: members/forms.py
    # LoginForm
    #  username, password를 받을 수 있도록 함
    #   password는 widget에 PasswordInput을 사용하기.
    if request.method == 'POST':
        pass
    else:
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'members/login.html', context)