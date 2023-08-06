# jcaptcha

## 安装
```
pip install jcaptcha 
```

## django view中使用

```
from jcaptcha.VerificationCode import jcaptcha

def create_code(request):
    text, result, file_path, image_data = jcaptcha()
    request.session['v_code'] = result
    return HttpResponse(image_data, content_type="image/png")

```

## uwsgi启动权限问题
