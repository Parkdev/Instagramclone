import os

from django.conf import settings
from django.http import HttpResponse, FileResponse


def media_serve(request, path):
    # 1. /media/로 시작하는 모든 URL은 이 view를 통해 처리
    # 2. /media/<뒤쪽 경로>/ 에서
    #    <뒤쪽 경로>부분을 path변수에 할당

    # 3. settings에 있는 MEDIA_ROOT를 기준으로
    #    <뒤쪽 경로>에 해당하는 파일의 경로를 file_path변수에 할당
    #       MEDIA_ROOT의 값 가져오는 법:
    #           django.conf import settings
    #           settings.MEDIA_ROOT
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    # 4. file_path를 open한 '파일객체'를
    #    FileResponse에 담아서 리턴
    #       ex) f = open(어딘가, 'rb')
    #           return FileResponse(f, content_type='image/jpeg')
    #
    #  -> content_type은 mimetypes라는 모듈로 동적으로 판단 가능
    #       mimetypes.guess_type(경로 또는 파일명)
    return FileResponse(open(file_path, 'rb'), content_type='image/jpeg')
