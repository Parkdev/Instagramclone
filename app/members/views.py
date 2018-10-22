from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from members.forms import LoginForm, SignupForm



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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request, user)
            return redirect('posts:post-list')


        # 1. request.POST 에 데이터가 옴
        # 2. 온 데이터 중에서 Username에 해당하는 값과 Password에 해당하는 값을 각각
        #    username, password변수에 할당
        # 3. 사용자 인증을 수행
        #   username/password에 해당하는 사용자가 있는지 확인
        # 4-1. 인증에 성공한다면
        #   세션/쿠키 기반의 로그인 과정을 수행, 완료 후 posts:post-list페이지로 redirect
        # 4-2. 인증에 실패한다면
        #   이 페이지에서 인증에 실패했음을 사용자에게 알려줌
    else:
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'members/login.html', context)

def logout_view(request):
    # URL: /members/logout/
    # Template: 없음

    # !POST요청일 때만 처리
    # 처리 완료 후 'posts:post-list'로 이동

    # base.html에 있는 'Logout'버튼이 이 view로의 POST요청을 하도록 함
    # -> form을 구현해야 함
    if request.method == 'POST':
        logout(request)
        return redirect('posts:post-list')


def signup_view(request):
    """
    render하는 경우
    1. POST요청이며 사용자명이 이미 존재할 경우
    2. POST요청이며 비밀번호가 같지 않는 경우
    3. GET요청인 경우
    redirect하는 경우
    1. POST요청이며 사용자명이 존재하지 않고 비밀번호가 같은 경우

    if request.method가 POST라면:
        if 사용자명이 존재하면;
            render1
        if 비밀번호가 같지 않으면;
            render2
        (else, POST면서 사용자명도없고 비밀번호도 같으면):
            redirect
    (else, GET요청이면):
        render

    if request.method가 POST라면:
        if 사용자명이 존재하면;
        if 비밀번호가 같지 않으면;
        (else, POST면서 사용자명도없고 비밀번호도 같으면):
            return redirect
    (POST면서 사용자명이 존재하면)
    (POST면서 비밀번호가 같지않으면)
    (POST면서 사용자명이 없고 비밀번호도 같은 경우가 "아니면" -> GET요청도 포함)
    return render
    """
    # URL: /members/signup/
    # Template: members/signup.html
    # Form:
    # SignupForm
    #   username, password1, password2를 받음
    # 나머지 요소들은 login.html의 요소를 최대한 재활용

    # GET요청시 해당 템플릿 보여주도록 처리
    # base.html에 있는 'Signup'버튼이 이 쪽으로 이동할 수 있도록 url 링크걸기
    form = SignupForm()
    context = {'form': form,
               'error': error}
    if request.method == 'GET':

        # form = SignupForm()
        # context = {
        #     'form': form,
        # }
        return render(request, 'members/signup.html', context)
    else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():

            error = f'{username}은 이미 사용중입니다.'


        if password1 != password2 :

            return HttpResponse('비밀번호와 비밀번호 확인란의 값이 일치하지 않습니다.')

        # create대신 create_user를사용하면 password를 해싱해줌
        user = User.objects.create_user(
            username=username,
            password=password1,
        )
        login(request, user)
        return redirect('posts:post-list')

    return render(request, 'members/signup.html', context)


        # 1. request.POST에 전달된 username, password1, password2를
        #    각각 해당 이름의 변수에 할당
        # 2-x에서는 HttpResponse에 문자열로 에러를 리턴해주기
        #  2-1 username에 해당하는 User가 이미 있다면
        #      사용자명 ({username})은 이미 사용중입니다.
        #  2-2. password1과 password2가 일치하지 않는다면
        #       비밀번호와 비밀번호 확인란의 값이 일치 하지 않습니다.
        # 3. 위의 두 경우가 아니라면
        #   새 User를 새엉, 해당 User로 로그인 시켜준 후 'post:post-list'로 redirect처리
