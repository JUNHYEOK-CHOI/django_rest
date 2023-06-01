from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Addresses
from .serializers import AddressesSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Addresses
from .serializers import AddressesSerializer
from rest_framework.parsers import JSONParser
# Create your views here.
from django.db import connection
import mysql.connector
import pymysql
from django.shortcuts import render
# Create your views here.

config = {
  'user': 'searchm',
  'password': 'dnfrkwhr12',
  'host': 'searchdb.cxihros2atcp.ap-northeast-2.rds.amazonaws.com',
  'port': '3306',
  'database': 'searchdb'
}

conn = mysql.connector.connect(**config)

cursor = conn.cursor()

# 쿼리 실행
query = "SELECT * FROM user"
cursor.execute(query)

# 결과 가져오기
results = cursor.fetchall()

# 결과 출력
for row in results:
    print(row)

# 연결 종료
cursor.close()
conn.close()


xx = []
yy = []

def index(request):
    return render(request, "addresses/index.html")

@csrf_exempt
def app_login(request):

    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))
        id = request.POST.get('userid', '')
        pw = request.POST.get('userpw', '')
        print("id = " + id + " pw = " + pw)


        for i in range(0, Addresses.user_num):
            if Addresses.user_list[i][0] == id and Addresses.user_list[i][1] == pw:
                result = 1
                break
            else:
                result = 0


        if result:
            print("로그인 성공!")
            return JsonResponse({'code': '0000', 'msg': '로그인성공입니다.'}, status=200)
        else:
            print("실패")
            return JsonResponse({'code': '1001', 'msg': '로그인실패입니다.'}, status=200)


@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))
        name = request.POST.get('username', '')
        id = request.POST.get('userid', '')
        pw = request.POST.get('userpw', '')
        print("name = " + name +"id = " + id + " pw = " + pw)

        result = 1

        for i in range(0, Addresses.user_num):
            if Addresses.user_list[i][0] == id:
                result = 0
                break


        if result:
            Addresses.user_list.append([id, pw, name])
            Addresses.user_num = Addresses.user_num + 1
            print("가입 성공!")
            return JsonResponse({'code': '0000', 'msg': '가입성공입니다.'}, status=200)
        else:
            print("가입 실패")
            return JsonResponse({'code': '1001', 'msg': '가입실패입니다.'}, status=200)

@csrf_exempt
def friend_list(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        id_list = []
        id_list2 = []
        id_num = 0
        for i in range(0, Addresses.friend_num):
            for j in range(0, Addresses.user_num):
                if Addresses.friend_list[i] == Addresses.user_list[j][0]:
                    id_list.append(Addresses.user_list[j][2])
                    id_list2.append(Addresses.user_list[j][0])
                    id_num = id_num + 1


        return JsonResponse({'code': id_list, 'code2': id_list2, 'num': id_num}, status=200)


@csrf_exempt
def user_list(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        id_list = []
        id_list2 = []
        id_num = 0
        id = request.POST.get('userid', '')

        for i in range(0, Addresses.user_num):
            if Addresses.user_list[i][0] == id:
                id_list.append(Addresses.user_list[i][0])
                id_list2.append(Addresses.user_list[i][2])
                id_num = id_num + 1

        return JsonResponse({'code': id_list, 'code2': id_list2, 'num': id_num}, status=200)

@csrf_exempt
def friend_list_add(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        FLAG = 0
        id = request.POST.get('userid', '')

        for i in range(0, Addresses.friend_num):
            if Addresses.friend_list[i] == id:
                FLAG = 1

        if(FLAG == 0):
            Addresses.friend_list.append(id)
            Addresses.friend_num = Addresses.friend_num + 1
            return JsonResponse({'code': '0000', 'msg': '추가 성공입니다.'}, status=200)
        else:
            return JsonResponse({'code': '1001', 'msg': '추가 실패입니다.'}, status=200)


@csrf_exempt
def history_list(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        return JsonResponse({'code': Addresses.history_friend, 'num': Addresses.history_num}, status=200)

@csrf_exempt
def history_list2(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        return JsonResponse({'code': Addresses.history_friend2, 'num': Addresses.history_num2}, status=200)


@csrf_exempt
def history_list3(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        return JsonResponse({'code': Addresses.history_friend3, 'msg': Addresses.history_num3}, status=200)


@csrf_exempt
def history_RT(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        user_id = request.POST.get('userid', '')
        user_name = ""

        for i in range(0, Addresses.user_num):
            if Addresses.user_list[i][0] == user_id:
                user_name = Addresses.user_list[i][2]
                break


        return JsonResponse({'code': user_name, 'msg': Addresses.history_RT_num}, status=200)


@csrf_exempt
def period_check(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        period = request.POST.get('period', '')
        check = request.POST.get('check', '')

        Addresses.checkList = check
        Addresses.period = period

        return JsonResponse({'code': '0000', 'msg': '성공입니다.'}, status=200)

@csrf_exempt
def period_check(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        period = request.POST.get('period', '')
        check = request.POST.get('check', '')

        Addresses.checkList = check
        Addresses.period = period

        return JsonResponse({'code': '0000', 'msg': '성공입니다.'}, status=200)

@csrf_exempt
def friend_list_delete(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        id = request.POST.get('userid', '')

        for i in range(0, Addresses.friend_num):
            if Addresses.friend_list[i] == id:
                Addresses.friend_list.remove(id)
                Addresses.friend_num = Addresses.friend_num - 1
                result = 1
                break
        if result:
            print("삭제 성공!")
            return JsonResponse({'code': '0000', 'msg': '삭제성공입니다.'}, status=200)
        else:
            print("삭제 실패")
            return JsonResponse({'code': '1001', 'msg': '삭제실패입니다.'}, status=200)

@csrf_exempt
def get_profile(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        id = request.POST.get('userid', '')
        result = 0

        for i in range(0, Addresses.user_num):
            if Addresses.user_list[i][0] == id:
                result = i
                break

        return JsonResponse({'name': Addresses.user_list[result][2], 'id': Addresses.user_list[result][0]}, status=200)

