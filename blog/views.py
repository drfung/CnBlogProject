from django.shortcuts import render
from django.http.response import HttpResponse,JsonResponse
from django.contrib import auth
import random

from .froms import UserForm
from .models import UserInfo

# Create your views here.
def login(request):
    if request.method == "POST":
        response = dict(user=None, msg=None)
        print(request.POST)
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code")
        valid_code_str = request.session.get('valid_code_str')
        print(valid_code,valid_code_str)

        if valid_code and valid_code.upper() == valid_code_str.upper():
            user = auth.authenticate(username = user, password = pwd)
            if user:
                auth.login(request,user)
                response['user'] = user.username
            else:
                response['msg'] = 'username or password error!'
        else:
            response["msg"] = "valid code error"
        return JsonResponse(response)

    return render(request,'blog/login.html')

def get_validCode_img(request):
    def get_random_color():
        return (random.randint(0,255),
                random.randint(0,255),
                random.randint(0,255)
                )
    # 方式一：
    # with open('854ac2b8ff452203.jpg', 'rb') as f:
    #     data = f.read()

    # 方式二： pip install pillow
    # from PIL import Image
    # img = Image.new("RGB", (270,40), color=get_random_color())
    #
    # with open('validCode.png', 'wb') as f:
    #     img.save(f, 'png')
    #
    # with open("validCode.png", 'rb') as f:
    #     data = f.read()

    # 方式三： 使用内存存储临时图片
    # from PIL import Image
    # from io import BytesIO
    # img = Image.new("RGB", (270, 40), color=get_random_color())
    # f = BytesIO()
    # img.save(f, 'png')
    # data = f.getvalue()

    # 方式四： 生成动态验证码
    # from PIL import Image,ImageDraw,ImageFont
    # from io import BytesIO
    # img = Image.new("RGB", (270, 40), color=get_random_color())
    # draw = ImageDraw.Draw(img)
    # xianxia_font = ImageFont.truetype('static/font/xianxia.ttf', size=32)
    # for i in range(5):
    #     random_num = str(random.randint(0,9))
    #     random_low_alpha = chr(random.randint(95,122))
    #     random_upper_alpha = chr(random.randint(65,90))
    #     random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
    #     draw.text((20+i*50,5), random_char, get_random_color(), font=xianxia_font)
    # f = BytesIO()
    # img.save(f, 'png')
    # data = f.getvalue()

    # 方式五： 添加噪点噪线
    from PIL import Image,ImageDraw,ImageFont
    from io import BytesIO
    img = Image.new("RGB", (270, 40), color=get_random_color())
    draw = ImageDraw.Draw(img)
    xianxia_font = ImageFont.truetype('static/font/xianxia.ttf', size=32)

    valid_code_str = ""
    for i in range(5):
        random_num = str(random.randint(0,9))
        random_low_alpha = chr(random.randint(95,122))
        random_upper_alpha = chr(random.randint(65,90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((20+i*50,5), random_char, get_random_color(), font=xianxia_font)
        valid_code_str += random_char
    request.session['valid_code_str'] = valid_code_str

    width = 270
    height = 40
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, x2, y1, y2),fill=get_random_color())
    for i in range(40):
        draw.point([random.randint(0,width), random.randint(0,height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x,y, x+4, y+4),0, 90, fill=get_random_color())

    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()

    return HttpResponse(data)

def index(request):
    return HttpResponse("ok")


def register(request):
    if request.is_ajax():
        # print(request.POST)
        response = {"user": None, "msg": None}
        form = UserForm(request.POST)
        if form.is_valid():
            response["user"] = form.cleaned_data.get("user")
            # 生成一条用户记录
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get('avatar')
            extra = {}
            if avatar_obj:
                extra["avatar"] = avatar_obj
            UserInfo.objects.create_user(username=user,password=pwd, email=email,**extra)
        else:
            # print(form.cleaned_data)
            # print(form.errors)
            response["msg"] = form.errors
        return JsonResponse(response)
    form = UserForm()
    return render(request, 'blog/register.html', {"form": form,})

