import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
import hashlib


# Create your views here.

def reg_view(request):
    # GET 返回页面
    if request.method == 'GET':
        return render(request, 'user/register.html')
    # POST 处理提交数据
    elif request.method == 'POST':
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        # 需要判断这个名称是否违规(这个用户名是否在数据库)
        old_users = User.objects.filter(username=username)
        if old_users:
            return HttpResponse('用户名已经注册')
        # 两个密码保持一致
        if password_1 == '':
            return HttpResponse('密码不能是空的')
        elif password_1 != password_2:
            return HttpResponse('密码不正确')
        # 密码使用密文
        m = hashlib.md5()
        m.update(password_1.encode())
        m_password = m.hexdigest()
        # 插入数据库
        try:
            # 有可能 报错 重复插入 (MySQL唯一索引, 注意并发问题)
            db_user = User.objects.create(username=username, password=m_password)
        except Exception as e:
            print('--create user error {}'.format(e))
            return HttpResponse('用户名已经注册')

        # 设置缓存, 10分钟免登陆
        request.session['username'] = username
        request.session['uid'] = db_user.id
        # TODO 修改session存储时间
        # return HttpResponse('注册成功')
        return  HttpResponseRedirect('/index')


def login_view(request):
    if request.method == 'GET':
        # 检查登陆状态, 如果登陆, 显示已登陆
        if request.session.get('username') and request.session.get('uid'):
            # return HttpResponse('已登录')
            return HttpResponseRedirect('/index')
        # 检查Cookies
        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        if c_username and c_uid:
            # 回写session
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            # return HttpResponse('已登录')
            return HttpResponseRedirect('/index')

        return render(request, 'user/login.html')

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            db_user = User.objects.get(username=username)
        except Exception as e:
            print('--login user error {}'.format(e))
            return HttpResponse('登陆失败: 用户名或密码错误?')

        # 判断用户密码是否正确
        m = hashlib.md5()
        m.update(password.encode())

        if m.hexdigest() != db_user.password:
            return HttpResponse('登陆失败: 用户名或密码错误!')

        # 记录会话状态
        request.session['username'] = username
        request.session['uid'] = db_user.id

        # 判断用户是否 点击了 选择记录用户名
        # result = HttpResponse('--- user login success---')
        result = HttpResponseRedirect('/index')
        if 'select' in request.POST:
            # cookies 中文编码处理
            username = json.dumps(username)
            result.set_cookie('username', username, 60 * 10)
            result.set_cookie('uid', db_user.id, 60 * 10)

        return result


def logout_view(request):
    # 退出登陆 删除session的值
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']

    # 响应对象
    resp = HttpResponseRedirect('/index')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')

    return resp
