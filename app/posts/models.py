import re

from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        # <AppName>.<ModelName>
        # 'members.User',
        # User,
        # auth.User을 쓴것과 완전히 같은 효과
        # 장고가 기본으로 제공하는 USER클래스
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    photo = models.ImageField(
        '사진',
        upload_to='post',
    )
    # auto_now_add: 객체가 처음 생성될때의 시간 저장
    # auto_now: 객체의 save()가 호출될 때 마다 시간 저장
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']


class Comment(models.Model):
    TAG_PATTERN = re.compile(r'#(?P<tag>\w+)')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='포스트',
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    content = models.TextField('댓글 내용')
    tags = models.ManyToManyField(
        'HashTag',
        blank=True,
        verbose_name='해시태그 목록',
    )

    # Comment의 save()가 호출 될 때,
    # content의 값을 사용해서 이 필드를 자동으로 채운 후 저장하기
    _html = models.TextField('태그가 HTML화된 댓글 내용', blank=True)

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):

        def save_html():
            # 저장하기 전에 _html필드를 채워야 함 (content갑을 사용해서)

            self._html = re.sub(self.TAG_PATTERN,
                   r'<a href="/explore/tags/\g<tag>/">#\g<tag></a>',
                   self.content,
                   )
        def save_tags():
            tags = [HashTag.objects.get_or_create(name=name)[0]
                    for name in re.findall(self.TAG_PATTERN, self.content)]
            self.tags.set(tags)

        # DB에 변경내역을 기록한 상
        save_html()
        super().save(*args, **kwargs)
        save_tags()

        # 자신의 'content'값에서 해시태그 목록을 가져와서
        # 자신의 'tags'속성 (MTM필드)에 할당




    @property
    def html(self):
        # 자신의 content속성값에서
        # "#태그명"에 해당하는 문자열을
        # 아래와 같이 변경
        # #문자열 -> <a herf="/explore/tags/{태그명}/">{태그명}</a>
        # re.sub을 사용
        return self._html

        # 템플릿에서는 comment.content대신 comment.html을 출력

        # 숙제
        # /explore/tags/{태그명}/ URL에서
        # 해당 태그를 가진 Post목록을 보여주는 view, url, template구현
        # URL name: tag-post-list
        # view:
        #       tag_po9st_list(request, tag_name)
        # template:
        #       /posts/tag_post_list.html

        #base.html에 있는 검색창에 값을 입력하고 Enter시 (Submit)
        # 해당 값을 사용해 위에서 만든 view로 이동


class HashTag(models.Model):
    name = models.CharField('태그명', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '해시태그'
        verbose_name_plural = f'{verbose_name} 목록'
