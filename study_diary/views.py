from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Diary, Daily, Monthly
from .forms import CreateDiary, CreateUser
import requests
import json

# 암호/인증
import bcrypt
import jwt

from webproject.settings import SECRET_KEY

import hashlib 

#from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt

#HTTP
from django.http import HttpResponse, JsonResponse
#from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .serializers import DiarySerializer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        request.session['login'] = False
        # try:
        id = request.POST['id']
        password = request.POST['password']

        # except(KeyError, name=='', password==''):
        #     context = {
        #         'uid':'empty',
        #         'upass' : 'empty',
        #     }
        #     return render(request,'login.html',context)

        #else:
        if User.objects.filter(id = id).exists():
# filter() : 특정 조건에 맞는 Row들을 가져오기 위해서는 filter() 메서드를 사용한다. 
# 예를 들어, 아래는 name 필드가 Kim 인 데이터만 가져온다.
            getUser = User.objects.get(id = id)
            if bcrypt.checkpw(password.encode('utf-8'), getUser.password.encode('utf-8')):
                token = jwt.encode({'id' : id}, SECRET_KEY, algorithm = "HS256")
                token = token.decode('utf-8')
                print(token)
                context = {
                    "result" : "success",
                    "token" : token
                }
                request.session['login'] = True
                request.session['user'] = id
                return render(request, 'index.html', {'context':context})
            else:
                request.session['login'] = False
                context = {
                    "result" : "wrong password"
                }
                return render(request, 'login.html', {'context':context})
        else:
            request.session['login'] = False
            context = {
                "result" : "no id"
            }
            return render(request, 'login.html', {'context':context})
        
        #return HttpResponse(json.dumps(context),content_type="application/json")
        #redirect('login')
        # json 데이터 형태로 변환하고 응답 보냄
    else:
        context = {
            "result" : "no post"
        }
        return render(request, 'login.html', {'context':context})

def logout(request):
    if request.session['user']:  # 로그인 중일 때
        del(request.session['user']) # session 없애기
    return redirect('/')

def join(request):
    if request.method == 'POST':
            pw = request.POST['password']
            pw = pw.encode('UTF-8')
            pw_encrypt = bcrypt.hashpw(pw, bcrypt.gensalt()).decode('utf-8')

            User(
                id = request.POST['id'],
                name = request.POST['name'],
                email = request.POST['email'],
                password = pw_encrypt
            ).save()
            #form = CreateUser(request.POST)
            return redirect('login')
    else:
        form = CreateUser()
        return render(request,'join.html',{'form':form})

def daily(request):
    user = User.objects.get(id = request.session.get('user'))
    if request.method == 'POST':
        date = request.POST.get('date')
        for i in range(15):
            daily = Daily()
            daily.date = date
            daily.writer = user
            daily.save()
    dailys_all = Daily.objects.filter(writer = user).order_by('-date','id')
    page = int(request.GET.get('page', 1)) #없으면 1로 지정
    paginator = Paginator(dailys_all, 60) #한 페이지 당 몇개 씩 보여줄 지 지정 
    dailys = paginator.get_page(page)
    return render(request, 'daily.html', {'dailys':dailys})



def daily_one(request, daily_date):
    user = User.objects.get(id = request.session.get('user'))
    if request.method == 'POST':
        date = request.POST.getlist('date')[0]
        print(date)
        for i in range(15):
            daily = Daily.objects.get(id = request.POST.getlist('id')[i])
            daily.category = request.POST.getlist('category')[i]
            daily.content = request.POST.getlist('content')[i]
            daily.check = request.POST.getlist('check')[i]
            if daily.category=='' and daily.content=='':
                daily.check = None
                daily.category = None
                daily.content = None
            daily.save()
        url = 'daily_one/' + date
        return redirect('daily')
    else:
        dailys = Daily.objects.filter(writer = user) & Daily.objects.filter(date = daily_date).order_by('id')

        return render(request, 'daily_one.html', {'dailys':dailys, 'date':daily_date})


def monthly(request):
    getUser = User.objects.get(id = request.session.get('user'))
    months_all = Monthly.objects.filter(writer = getUser)
    return render(request, 'monthly.html',{'data':months_all})
    

def monthly_add(request):
    user = User.objects.get(id = request.session.get('user'))
    if request.method == 'POST':
        Monthly(
            date = request.POST['date'],
            content = request.POST['content'],
            writer = user
        ).save()
    return redirect('monthly')



def diary(request):
    getUser = User.objects.get(id = request.session.get('user'))
    diarys_me = Diary.objects.filter(writer = getUser).order_by('-date')
    diarys_others = Diary.objects.filter(is_public = 2).order_by('-date')

    page = int(request.GET.get('page', 1)) #없으면 1로 지정
    paginator = Paginator(diarys_me, 15) #한 페이지 당 몇개 씩 보여줄 지 지정 
    paginator2 = Paginator(diarys_others, 15) 

    diarys_me = paginator.get_page(page)
    diarys_others = paginator2.get_page(page)
    num = 15

    
    return render(request, 'diary.html', {'diarys_me':diarys_me, 'diarys_others':diarys_others,'num' :num})


def diary_one(request, diary_id):
    user = User.objects.get(id = request.session.get('user'))
    #diarys = Diary.objects.filter(writer = getUser).order_by('-date')
    diarys_all = Diary.objects.filter(writer = user).order_by('-date')
    page = int(request.GET.get('page', 1)) #없으면 1로 지정
    paginator = Paginator(diarys_all, 25) #한 페이지 당 몇개 씩 보여줄 지 지정 
    diarys = paginator.get_page(page)
    diary_one = get_object_or_404(Diary, pk = diary_id)

    return render(request, 'diary_one.html', {'diarys':diarys, 'diary_one':diary_one})

def diary_one_update(request, diary_id):
    user = User.objects.get(id = request.session.get('user'))
    diary = get_object_or_404(Diary, pk = diary_id, writer = user)

    if request.method == "POST":
        form = CreateDiary(request.POST, instance=diary)
        if form.is_valid():
            diary = form.save(commit = False)
            diary.save()
            return redirect('/diary/'+str(diary_id))
    #diarys = Diary.objects.filter(writer = getUser).order_by('-date')
    else:
        diary = Diary.objects.get(id = diary_id)
        if diary.writer == user:
            form = CreateDiary(instance = diary)
            context = {
                'form':form,
                'state':'일기 수정'
            }
        return render(request, 'diary_write.html', context)

def diary_one_delete(request, diary_id):
    user = User.objects.get(id = request.session.get('user'))
    #diarys = Diary.objects.filter(writer = getUser).order_by('-date')
    diary_one = get_object_or_404(Diary, pk = diary_id)
    print(diary_one.title)
    diary_one.delete()

    return redirect('diary')

def diary_write(request):
    if request.method == 'POST':
        form = CreateDiary(request.POST)
        
        user_id = request.session.get('user')
        user = User.objects.get(id = user_id)
        print(user)

        if form.is_valid():
            diary = Diary(date = str(form.cleaned_data['date']), writer = user, title = form.cleaned_data['title'], content = form.cleaned_data['content'])
            diary.save()

            return redirect('diary')
        else:
            return redirect('diary_write')
    else:
        form = CreateDiary()
        context = {
            'form':form,
            'state':'일기 쓰기'
        }
        return render(request,'diary_write.html',context)

    
def chart(request):
    user_id = request.session.get('user')
    user = User.objects.get(id = user_id)

    dailys = Daily.objects.filter(writer = user)
    
    # 같은 category별로 count 
    dailys = dailys.values('category')\
                        .order_by('category')\
                        .filter(~Q(category= None))\
                        .filter(Q(check=2))\
                        .annotate(count=Count('category'))\
                        .order_by('-count') #위의 count로 내림차순

    # NULL이 아닌 category 수 세기
    count_all = Daily.objects.filter(~Q(category= None)).count()
    print(dailys)
    chart = {} # dict
    for daily in dailys:
        print(daily)
        chart[daily['category']] = daily['count']
    print(chart)
    
    # xdata = dailys.values('category') # queryset을 배열로 # label이라 할수 있음
    # ydata = dailys.values('count')

    # extra_serie = {"category": {"y_start": "", "y_end": " cal"}}
    # chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    # charttype = "pieChart"

    # data = {
    #     'charttype': charttype,
    #     'chartdata': chartdata,
    # }

    print(dailys.count())
    print(type(dailys))

    # print(xdata)
    return render(request, 'chart.html', {'dailys' : dailys, 'count_all' : count_all,  'chart':json.dumps(chart,ensure_ascii=False) })

# restframework
# 특정 뷰에 대해 csrf를 적용하고 싶지 않다
@api_view(['GET', 'POST'])
@csrf_exempt
def diary_rest(request):
    if request.method == 'GET':
        queryset = Diary.objects.all()
        serializer = DiarySerializer(queryset, many=True)
        return Response(serializer.data)
        #return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})
        # json_dumps_param: ensure ~~ : 한글깨짐해결

    if request.method == 'POST':
        print("post 옴")
        serializer = DiarySerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print("serializer: valid")
            serializer.save()
            print("post 완료")

            return Response(serializer.data)
        return Response(serializer.errors)


        # REST 프레임워크에서는 기존 HttpRequest의 확장 오브젝트인 Request를 소개하고,
        # 좀더 융통성있는 request 파싱을 지원합니다. 
        # Request 오브젝트의 핵심적인 속성은 request.POST와 비슷한 역할을 하고 
        # Web API들과 좀더 유용하게 동작하는 request.data 