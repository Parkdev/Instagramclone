from django import forms

from .models import Post, Comment


class PostCreateForm(forms.Form):
    photo = forms.ImageField(
        # 이 필드는 파일입력 위젯을 ㅏ용
        widget=forms.FileInput(
            # HTML위젯의 속성 설정
            # form-control-file클래스를 사용
            attrs={
                'class': 'form-control-file',
            }
        )
    )
    comment = forms.CharField(
        #반드시 채워져 있을 필요는 없
        required=False,
        # HTML랜더링 위젯으로 textarea를 사용
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    def save(self, **kwargs):
        post = Post.objects.create(
            photo=self.cleaned_data['photo'],
            **kwargs,
        )



        # 1. Post생성시 Comment생성 (선택적)
        # 만약에 comment항목이 있다면
        # 생성한 Post에 연결되는 Comment를 생성
        # author=request.user 생성한 Post의 author와 동일
        # post=post가 되도록, 생성한 Post

        # 2. post_list에서 각 Post의 댓글 목록을 출력
        comment_content = self.cleaned_data.get('comment')
        if comment_content:

            post.comments.create(
                author=post.author,
                content=comment_content,
            )
        
        return post

class CommentCreateForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows' : 2,
            }
        )
    )

    def save(self, post, **kwargs):
        content = self.cleaned_data['content']
        return post.comments.create(
            content=content,
            **kwargs,
        )

class PostForm(forms.ModelForm):
    # 1. posts.views.post_create
    # 2. templates/posts/post_create.html

    comment = forms.CharField(
        label='내용',
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Post
        fields = [
            'photo',
        ]
        widgets = {
            'photo' : forms.ClearableFileInput(
                attrs={
                    'class': 'form-control-file'
                }
            )
        }

class CommentForm(forms.ModelForm):
    # Comment Model클래스를 사용하는 ModelForm 구현
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2,
                }
            )
        }
    pass