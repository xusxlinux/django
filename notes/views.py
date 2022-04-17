from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import csv


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
        # content = request.POST.get('content')

        from .models import Notes
        # uid是数据库的user表的id
        Notes.objects.create(title=title, content=content, user_id=uid)
        # return HttpResponseRedirect('/notes/list_note')
        return HttpResponseRedirect('/index')


# 分页 + 修改
def list_note(request):
    # /list_note?page=1 使用查询字符串

    # 这个all_note 我可以使用ORM, 取数据库中的表数据
    from .models import Notes
    all_notes = Notes.objects.get_queryset().all()

    # 导入类库 paginator类
    from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage
    paginator = Paginator(all_notes, 10)

    # 初始化 具体页码的 page对象
    page_number = request.GET.get('page', 1)
    c_page = paginator.page(int(page_number))

    return render(request, 'notes/list_note.html', locals())


# 下载数据
def test_csv(request):
    # 响应头
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="mydata.csv"'

    writer = csv.writer(response)
    writer.writerow(['title', 'content'])

    from .models import Notes
    notes_info = Notes.objects.all()

    for n in notes_info:
        writer.writerow([n.title, n.content])

    return response


# 分页下载数据
def make_csv_view(request):
    from .models import Notes
    notes_info = Notes.objects.all().order_by('title')
    # all_notes = Notes.objects.get_queryset().all()

    # 导入类库 paginator类
    from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage
    paginator = Paginator(notes_info, 10)

    # 初始化 具体页码的 page对象
    page_number = request.GET.get('page', 1)
    c_page = paginator.page(int(page_number))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="mydata-%s.csv"'%(page_number)

    writer = csv.writer(response)
    writer.writerow(['title', 'content'])

    for n in c_page:
        writer.writerow([n.title, n.content])
    return response