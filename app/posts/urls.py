from django.urls import path

from . import views

# 이 urls모듈의 app_name에 'posts'를 사용
# reverse또는 템플릿의 {% url %}태그에서 사용
app_name = 'posts'

urlpatterns = [
    # posts.urls내의 패턴들은, prefix가 '/posts/'임
    path('',
         views.post_list,
         name='post-list'),
    path('create/',
         views.post_create,
         name='post-create'),
]
