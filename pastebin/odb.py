import time
import random
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import csrf
from model.models import database


def testdb(request):
    op = database(text='23333', index=1)
    op.save()
    return HttpResponse("Save!")


def add_text(request):
    re = {'title': 'PasteBin'}  # 返回到view的set
    host = request.get_host()
    print(request.POST['password'])
    '''d41d8cd98f00b204e9800998ecf8427e'''
    if request.POST:  # 仅接受post请求
        if request.POST['text']:  # 文本不为空
            re['default'] = '链接：'
            re['r'] = 'http://' + host + '/text?id='
            dic = {
                'text': request.POST['text'],
                'delete': 0, 'date': 0,
                'password': request.POST['password'],
                   }  # 数据库操作命令
            index = random.randint(0, 9223372036854775807)
            f = database.objects.filter(index=index)
            while f:
                index = random.randint(0, 9223372036854775807)
                f = database.objects.filter(index=index)
            re['r'] += str(index)
            dic['index'] = index
            re['r'] += request.POST['password']

            checkbox = request.POST.getlist('checkbox')
            for value in checkbox:  # 判断是否选择附加功能
                if value == '1':
                    dic['delete'] = 1
                if value == '2':
                    dic['date'] = int(time.time())+86400
            database.objects.create(**dic)  # 执行数据库操作
        else:
            re['default'] = '请输入非空内容！'
    return render(request, 'index.html', re)


def search_from_index(request):
    request.encoding = 'utf-8'
    re = {'title': '文本内容——PasteBin'}
    if 'id' in request.GET and request.GET['id']:
        result = database.objects.filter(index=request.GET['id'])
        # 由index查询数据库
        if result:  # 检查数据库是否有记录
            if result[0].delete != -1:
                '''
                判断是否是阅后即焚
                0：未设置
                1：已设置
                -1：已销毁
                '''
                re['text'] = result[0].text
                if result[0].delete == 1:  # 如果设置阅后即焚就销毁
                    result.update(delete=-1, date=int(time.time()))
            else:  # 读取销毁时间并返回到视图
                t = time.localtime(result[0].date)
                re['text'] = '该消息已被销毁！（销毁时间：'+time.strftime("%Y-%m-%d %H:%M:%S", t)+'）'
                return render(request, 'text.html', re)
            if result[0].date:  # 判断消息是否到期（数据库中以10位时间戳存储）
                if int(time.time()) > result[0].date:
                    t = time.localtime(result[0].date)
                    re['text'] = '该消息已过期！（销毁时间：'+time.strftime("%Y-%m-%d %H:%M:%S", t)+'）'
        else:  # 在数据库中没找到数据
            re['text'] = 'id错误，请检查是否复制失误'
    else:  # 没传入id
        re['text'] = '数据错误！'
    return render(request, 'text.html', re)
