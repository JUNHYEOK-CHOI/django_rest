from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # MySQL에서 사용자 조회
        query = "SELECT id, name, password FROM user WHERE id = %s AND password = %s"
        values = (id, pw)
        cursor.execute(query, values)
        user_data = cursor.fetchone()  # 사용자 정보 조회

        # 사용자 인증 성공
        if user_data:
            print("로그인 성공!")
            return JsonResponse({'code': '0000', 'msg': '로그인 성공입니다.'}, status=200)
        # 사용자 인증 실패
        else:
            print("로그인 실패")
            return JsonResponse({'code': '1001', 'msg': '로그인 실패입니다.'}, status=200)

@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        id = request.POST.get('userid', '')
        pw = request.POST.get('userpw', '')
        name = request.POST.get('username', '')
        # 추가적인 회원 가입 정보를 가져올 수 있습니다.

        # user = authenticate(request, username=username, password=password)

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # INSERT 쿼리 실행
        query = "INSERT INTO user (id, name, password) VALUES (%s, %s, %s)"
        values = (id, name, pw)
        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        return JsonResponse({'code': '0000', 'msg': '회원 가입 성공입니다.'}, status=200)

@csrf_exempt
def show_friend_list(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        name_list = [] # name 을 저장
        id_list = [] # id를 저장
        id_num = 0

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 현재 사용자의 ID
        user_id = request.POST.get('user_id')

        # friend 테이블에서 현재 사용자의 친구들 조회
        query = f"SELECT friend_id FROM friend WHERE id = '{user_id}'"
        cursor.execute(query)
        results = cursor.fetchall()

        # 친구들의 정보 조회
        for result in results:
            friend_id = result[0]
            query = f"SELECT name FROM user WHERE id = '{friend_id}'"
            cursor.execute(query)
            friend_info = cursor.fetchone()

            if friend_info:
                name = friend_info[0]  #code name / code2 id
                name_list.append(name)
                id_list.append(friend_id)
                id_num += 1

        # 연결 종료
        cursor.close()
        conn.close()

        print(name_list)

        return JsonResponse({'code': name_list, 'code2': id_list, 'num': id_num}, status=200)


@csrf_exempt
def user_list(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        id_list = []
        name_list = []
        id_num = 0
        id = request.POST.get('userid', '')

        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # SELECT 쿼리 실행
        query = "SELECT u.id, u.name FROM user u WHERE u.id = %s"
        cursor.execute(query, (id,))

        # 결과 가져오기
        results = cursor.fetchall()

        # 결과 처리
        for row in results:
            id_list.append(row[0])
            name_list.append(row[1])
            id_num += 1

        cursor.close()
        conn.close()

        return JsonResponse({'code': id_list, 'code2': name_list, 'num': id_num}, status=200)

@csrf_exempt
def friend_add(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        id = request.POST.get('userid', '')
        friend_id = request.POST.get('friendid', '')

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 사용자 ID가 존재하는지 확인
        query = f"SELECT id FROM user WHERE id = '{id}'"
        cursor.execute(query)
        result = cursor.fetchone()

        print(id+"   "+friend_id)

        if result:
            # 친구 목록에 사용자 ID 추가
            query = f"INSERT INTO friend (id, friend_id) VALUES ('{id}', '{friend_id}')"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()
            return JsonResponse({'code': '0000', 'msg': '친구 추가 성공입니다.'}, status=200)
        else:
            cursor.close()
            conn.close()
            return JsonResponse({'code': '1001', 'msg': '친구 추가 실패입니다.'}, status=200)


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
def friend_delete(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        id = request.POST.get('userid', '')
        friend_id = request.POST.get('friendid', '')

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 사용자 ID가 존재하는지 확인
        query = f"SELECT id, friend_id FROM friend WHERE id = '{id}' AND friend_id = '{friend_id}'"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            # 친구 목록에서 사용자 ID 삭제
            query = f"DELETE FROM friend WHERE id = '{id}' AND friend_id = '{friend_id}'"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()
            return JsonResponse({'code': '0000', 'msg': '친구 삭제 성공입니다.'}, status=200)
        else:
            cursor.close()
            conn.close()
            return JsonResponse({'code': '1001', 'msg': '친구 삭제 실패입니다.'}, status=200)

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

