import io
import json
from pprint import pprint

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect

import requests

User = get_user_model()

# Create your views here.
from members.forms import LoginForm, SignupForm, UserProfileForm


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

    #username, password를 받는 부분
    # LoginForm을 사용하도록 수정
    # 로그인에 실패했을 경우, Template에 form.non_filed_errors를 사용해서
    # 로그인에 실패했다는것을 출력\
    context = {}
    if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)
        form = LoginForm(request.POST)
        if form.is_valid():
            # 주어진 username, password로
            # authenticate에 성공했다
            # request와 authenticate된 user를 사용해서
            # login()처리 후
            login(request, form.user)
            # GET parameter에 'next'가 전달되었다면
            # 해당 키의 값으로 redirect
            # 전달되지 않았으면 'posts:post-list'로 redirect
            next_path = request.GET.get('next')
            if next_path:
                return redirect(next_path)
            return redirect('posts:post-list')
    else:
        form = LoginForm()
    context['form'] = form
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
    context = {}
    if request.method == 'POST':
        # POST로 전달된 데이터를 확인
        # 올바르다면 User를 생성하고 Post-list화면으로 이동
        # (is_valid()가 True면 올바르다고 가정)
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            # user = User.objects.create_user(
            #     username=form.cleaned_data['username'],
            #     password=form.cleaned_data['password1'],
            # )
            login(request, user)
            return redirect('posts:post-list')

    # GET요청시 또는 POST로 전달된 데이터가 올바르지 않을 경우
    # signup.html에
    #   빈 Form또는 올바르지 않은 데이터에 대한 정보가
    #  포함된 Form을 전달해서 동적으로 form을 렌더링
    else:
        form = SignupForm()
    context['form'] = form
    return render(request, 'members/signup.html', context)

@login_required
def profile(request):

    # POST요청시에는 현재 로그인한 유저의 값을
    # POST요청에 담겨온 값을 사용해 수정
    # 이후 다시 form을 보여줌
    #   f = Form(request.POST,
    #            request.FILES,
    #            instance=<수정할 인스턴스>)

    # GET요청시에는 현재 로그인한 유저의 값을 가진
    # Form을 보여줌
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # https://docs.djangoproject.com/ko/2.1/ref/contrib/messages/
            # is_valid()를 통과하고 인스턴스 수정이 완료되면
            # messages모듈을 사용해서 템플릿에 수정완료 메세지를 표시
            messages.success(
                request,
                '프로필 수정이 완료되었습니다',
            )



    form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
    }

    return render(request, 'members/profile.html', context)

def facebook_login(request):
    api_base = 'https://graph.facebook.com/v3.2'
    api_get_access_token = f'{api_base}/oauth/access_token'
    api_me = f'{api_base}/me'

    # URL: /members/facebook-login/
    # URL name: 'members:facebook-login'
    # request.GET에 전달된 'code'값을
    #   그대로 HttpResponse로 출력

    # 페이스북 로그인 버튼의 href안에 있는 'redirect_uri'값을
    # 이 view로 오도록 설정

    #request token
    code = request.GET.get('code')

    # request token을 access token으로 교환
    # 엑세스 토큰 교환 엔드포인트에
    # requests를 사용해서 GET요청
    # 이후 돌아온 response.text를
    # HttpResponse로 보여주기
    # response = requests.get(f'https://graph.facebook.com/v3.2/oauth/access_token?'
    #                         f'client_id=505053883344168'
    #                         f'&redirect_uri=http://localhost:8000/members/facebook-login'
    #                         f'&client_secret=ebb5291bee726882d7cf5da0906b1352'
    #                         f'&code={code}')

    #더깔끔하게
    params = {
        'client_id': 505053883344168,
        'redirect_uri': 'http://localhost:8000/members/facebook-login/',
        'client_secret': 'ebb5291bee726882d7cf5da0906b1352',
        'code': code,
    }
    response = requests.get(api_get_access_token, params)
    # 인수로 전달한 문자열이 'JSON' 형식일 것으로 생각
    # json.loades는 전달한 문자열이 JSON형식일 경우, 해당 문자열을 파싱해서 파이썬 object를 리턴함
    # response_object = json.loads(response.text)
    # data = response.json()
    # access token = data['access_token']
    #
    # return HttpResponse('{}, {}'.format(
    #     response_object,
    #     type(response_object),
    # ))

    data = response.json()
    access_token = data['access_token']

    params = {
        'access_token': access_token,
        'fields' : ','.join([
            'id',
            'first_name',
            'last_name',
            'picture.type(large)',
        ]),
    }

    response = requests.get(api_me, params)
    data = response.json()

    facebook_id = data['id']
    first_name = data['first_name']
    last_name = data['last_name']
    url_img_profile = data['picture']['data']['url']

    # HTTP GET요청의 응답을 받아옴
    img_response = requests.get(url_img_profile)
    img_data = img_response.content


    # 응답의 binary data를 사용해서 In-memory binary stream(file)객체를 생성
    # f = io.BytesIO(img_response.content)
    f = SimpleUploadedFile(img_response,)

    User.objects.create_user(
        username=facebook_id,
        first_name=first_name,
        last_name=last_name,
        img_profile=img_response.content,

    )
    # pprint(data)
    # return HttpResponse('{}<br>{}'.format(str(data), response.url))
    return HttpResponse(data)