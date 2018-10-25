from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from .forms import PostCreateForm
from .models import Post


def post_list(request):
    # 1. Post모델에
    #  created_at (생성시간 저장)
    #       auto_now_add=True
    #  modified_at (수정시간 저장)
    #       auto_now=True
    #   두 필드를 추가

    # 2. Post모델이 기본적으로 pk내림차순으로 정렬되도록 설정
    #     class Meta:
    #         ordering = ['-pk']

    # 3. 모든 Post객체에 대한 QuerySet을
    #    render의 context인수로 전달 (키: posts)
    #      context = {'posts': Post.objects.all()}

    # 4. posts/post_list.html을 Template으로 사용
    #     템플릿에서는 posts값을 순회하며
    #     각 Post의 photo정보를 출력

    # 5. url은 posts.urls모듈을 사용
    #    config.urls에서 해당 모듈을 include
    #    posts.urls.app_name = 'posts'를 사용
    #     include할 URL은 'posts/'
    #     view의 URL은 비워둔다
    #      결과: localhost:8000/posts/ 로 접근시
    #            이 view가 처리하도록 함
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post_list.html', context)

@login_required
def post_create(request):
    # if not request.user.is_authenticated:
    #     return redirect('members:login')

    context = {}
    if request.method =='POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(author=request.user)
            return redirect('posts:post-list')

    else:
        form = PostCreateForm()

    context['form'] = form
    return render(request, 'posts/post_create.html', context)

def comment_create(request,post_pk):
    """
    post_pk에 해당하는 Post에 댓글을 생성하는 view
    'POST'메서드 요청만 처리

    'content'키로 들어온 값을 사용해 댓글 생성, 작성자는 요청한 User
    URL: /posts/<post_pk>/comments/create/

    댓글 생성 완료 후에는 posts:post-list로 redirect


    :param request:
    :param post_pk:
    :return:
    """
    # context={}
    # if request.method == 'POST':
    #     form =
    #     if form.is_valid():
    #         form.save(author=request.user)
    #         return redirect('posts:post-list')
    pass