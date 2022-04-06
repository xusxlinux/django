from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# Create your views here.

# 装饰器 校验登陆状态
def check_login(fn):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            # 检查cookies
            c_username = request.COOKIES.get('username')
            c_uid = request.session.get('uid')
            if not c_username or not c_uid:
                return HttpResponseRedirect('/user/login')
            else:
                # 因为cookies有缓存, session没有缓存, 所以要回写session
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return fn(request, *args, **kwargs)
    return wrap


@check_login
def add_note(request):
    if request.method == 'GET':
        return render(request, 'notes/add_note.html')

    elif request.method == 'POST':
        # 处理数据
        uid = request.session['uid']
        title = request.POST['标题']
        content = request.POST['content']


        from .models import Notes
        # uid是数据库的user表的id
        Notes.objects.create(title=title, content=content, user_id=uid)

        return HttpResponse('添加笔记成功')