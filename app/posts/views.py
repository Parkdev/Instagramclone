import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from .forms import PostCreateForm, CommentCreateForm, CommentForm, PostForm
from .models import Post, Comment, HashTag


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
    # 적절히 CommentCreateForm을 전달
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }
    return render(request, 'posts/post_list.html', context)

@login_required
def post_create(request):
    # if not request.user.is_authenticated:
    #     return redirect('members:login')

    context = {}
    if request.method =='POST':
        # form = PostCreateForm(request.POST, request.FILES)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save(author=request.user)
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            comment_content = form.cleaned_data['comment']
            if comment_content:
                #위에서 생성한 Post에 연결되는 Comment생성
                post.comments.create(
                    author=request.user,
                    content=comment_content,
                )
            return redirect('posts:post-list')

    else:
        form = PostForm()

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
    # 1. post_pk에 해당하는 Post 객체를 가져와 post변수에 할당
    # 2. request.POST에 전달된 'content'키의 값을 content변수에 할당
    # 3. Comment생성
    #   author: 현재 요청의 User
    #   post: post_pk에 해당하는 Post객체
    #   content: request.POST로 전달된 'content'키의 값
    # 4. post:post-list로 redirect
    if request.method == 'POST':

        # post = Post.objects.get(pk=post_pk)

        # posts.forms.CommentCreateForm() 을 사용
        # form = CommentForm(request.POST)
        # if form.is_valid():
        #   form.save(author=request.user, post=post)
        post = Post.objects.get(pk=post_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            # form.save(author=request.user, post=post)
            # 모델폼을 쓰면 위가 아래처럼바뀐다. (CommentForm)
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()


            # comment가 가진 content속성에서
            # 해시태그에 해당하는 문자열들을 가져와서
            # HashTag객체를 가져오거나 생성 (get_or_create)
            # 이후 comment.tags에 해당 객체들을 추가

            p = re.compile(r'#(?P<tag>\w+)')
            # tag_string_list = re.findall(p, comment.content)
            # tag_list =[]
            # for tag_string in tag_string_list:
            #     tag = HashTag.objects.get_or_create(
            #         name=tag_string,
            #     )[0]
            #
            #     tag_list.append(tag)
            #     comment.tags.set(tag_list)
            tags = [HashTag.objects.get_or_create(name=name)[0] for name in re.findall(p, comment.content)]
            comment.tags.set(tags)


            return redirect('posts:post-list')

        # content = request.POST['content']
        # Comment.objects.create(
        #     post = post,
        #     author = request.user,
        #     content = content,
        # )
        # return redirect('posts:post-list')