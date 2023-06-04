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
            update_query = "UPDATE user SET alive = 'Y' WHERE id = %s"
            update_values = (id,)
            cursor.execute(update_query, update_values)
            conn.commit()
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

        name_list = []  # name 을 저장
        id_list = []  # id를 저장
        id_num = 0

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 현재 사용자의 ID
        user_id = request.POST.get('userid')
        print(user_id)

        # friend 테이블에서 현재 사용자의 친구들 조회
        query = f"SELECT friend_id FROM friend WHERE id = '{user_id}'"
        cursor.execute(query)
        results = cursor.fetchall()

        print(results)

        # 친구들의 정보 조회
        for result in results:
            friend_id = result[0]
            query = f"SELECT name FROM user WHERE id = '{friend_id}'"
            cursor.execute(query)
            friend_info = cursor.fetchone()

            if friend_info:
                name = friend_info[0]  # code name / code2 id
                name_list.append(name)
                id_list.append(friend_id)
                id_num += 1

        # 연결 종료
        cursor.close()
        conn.close()

        print(name_list)
        print(id_list)
        print(id_num)

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

        print(id + "   " + friend_id)

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
def history_list(request):  # 예전의 기록들
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        name_list = []  # name 을 저장
        id_list = []  # id를 저장
        id_num = 0

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 현재 사용자의 ID
        user_id = request.POST.get('userid')
        print(user_id)

        # friend 테이블에서 현재 사용자의 친구들 조회
        query = f"SELECT friend_id FROM friend WHERE id = '{user_id}'"
        cursor.execute(query)
        results = cursor.fetchall()

        print(results)

        # 친구들의 정보 조회
        for result in results:
            friend_id = result[0]
            query = f"SELECT name FROM user WHERE id = '{friend_id}'"
            cursor.execute(query)
            friend_info = cursor.fetchone()

            if friend_info:
                name = friend_info[0]  # code name / code2 id
                name_list.append(name)
                id_list.append(friend_id)
                id_num += 1

        # 연결 종료
        cursor.close()
        conn.close()

        print(name_list)
        print(id_list)
        print(id_num)

        return JsonResponse({'code': name_list, 'code2': id_list, 'num': id_num}, status=200)


@csrf_exempt
def history_list2(request):  # 각 친구별 여행 목록
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        user_id = request.POST.get('userid', '')  # 사용자 ID

        # MySQL에서 사용자의 유일한 레코드 이름 조회
        query = "SELECT DISTINCT record_name FROM user_history WHERE id IN (SELECT allow_fid FROM allow_friend WHERE allow_fid = %s)"
        values = (user_id,)
        cursor.execute(query, values)
        records = cursor.fetchall()  # 사용자의 레코드 목록 조회

        # 유일한 레코드 이름 개수
        num_records = len(records)

        # 레코드 출력
        record_names = [record[0] for record in records]
        print("레코드 목록:", record_names)

        return JsonResponse({'code': user_id, 'num': num_records, 'records': record_names}, status=200)


@csrf_exempt
def history_list3(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        user_id = request.POST.get('userid', '')  # 사용자 ID
        record_name = request.POST.get('recordname', '')  # 사용자 record 정보

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # MySQL에서 사용자의 이름 조회
        name_query = "SELECT name FROM user WHERE id = %s"
        name_values = (user_id,)
        cursor.execute(name_query, name_values)
        name = cursor.fetchone()[0]  # 사용자 이름 조회

        # MySQL에서 record_name에 해당하는 longitude와 latitude 조회
        history_query = "SELECT longitude, latitude FROM user_history WHERE record_name = %s"
        history_values = (record_name,)
        cursor.execute(history_query, history_values)
        longitude_latitude = cursor.fetchall()  # record_name에 해당하는 longitude와 latitude 조회

        longitude_list = []
        latitude_list = []

        for row in longitude_latitude:
            longitude_list.append(row[0])  # longitude 값을 리스트에 추가
            latitude_list.append(row[1])  # latitude 값을 리스트에 추가

        print(longitude_list)
        print(latitude_list)

        return JsonResponse({'name': name, 'longitude': longitude_list, 'latitude': latitude_list}, status=200)


@csrf_exempt
def history_RT(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        user_id = request.POST.get('userid', '')  # 사용자 ID

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # MySQL에서 사용자의 이름 조회
        name_query = "SELECT name FROM user WHERE id = %s"
        name_values = (user_id,)
        cursor.execute(name_query, name_values)
        name = cursor.fetchone()[0]  # 사용자 이름 조회

        # MySQL에서 record_name에 해당하는 longitude, latitude, time 조회
        history_query = "SELECT longitude, latitude, time FROM user_history WHERE alive = 'Y' ORDER BY history_id ASC LIMIT 1"
        cursor.execute(history_query)
        longitude_latitude_time = cursor.fetchone()  # record_name에 해당하는 longitude, latitude, time 조회

        print(longitude_latitude_time)

        longitude_list = []
        latitude_list = []
        record_time = None

        if longitude_latitude_time:
            longitude_list.append(longitude_latitude_time[0])  # longitude 값을 리스트에 추가
            latitude_list.append(longitude_latitude_time[1])  # latitude 값을 리스트에 추가
            record_time = longitude_latitude_time[2]  # time 값을 저장

        print(longitude_list)
        print(latitude_list)

        return JsonResponse({'name': name, 'longitude': longitude_list, 'latitude': latitude_list},
                            status=200)


@csrf_exempt
def update_alive_status(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        user_id = request.POST.get('userid', '')  # 사용자 ID

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # alive 값을 'N'으로 업데이트하는 쿼리 실행
        update_query = "UPDATE user_history SET alive = 'N' WHERE id = %s AND alive = 'Y'"
        update_values = (user_id,)
        cursor.execute(update_query, update_values)

        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        return JsonResponse({'code': '0000', 'msg': '성공입니다.'}, status=200)


@csrf_exempt
def period_check(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        id = request.POST.get('id', '')
        record_name = request.POST.get('recordname', '')
        allow_fids = request.POST.getlist('allow_fid')

        # Insert the data into the allow_friend table
        query = "INSERT INTO allow_friend (id, record_name, allow_fid) VALUES (%s, %s, %s)"
        values = [(id, record_name, allow_fid) for allow_fid in allow_fids]
        cursor.executemany(query, values)

        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        return JsonResponse({'code': '0000', 'num': '성공입니다.'}, status=200)


@csrf_exempt
def period_check2(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        id = request.POST.get('id', '')
        longitude = request.POST.get('longitude', '')
        latitude = request.POST.get('latitude', '')
        record_name = request.POST.get('recordname', '')
        period = request.POST.get('period', '')

        # Insert the location data into the user_history table
        query = "INSERT INTO user_history (id, longitude, latitude, record_name, period, alive) VALUES (%s, %s, %s, %s, %s, 'Y')"

        values = (id, longitude, latitude, record_name, period)

        cursor.execute(query, values)

        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        return JsonResponse({'code': '0000', 'num': '성공입니다.'}, status=200)



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
        name = ""

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # SELECT 쿼리 실행
        query = "SELECT name FROM user WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()

        if result:
            name = result[0]

        # 연결 종료
        cursor.close()
        conn.close()

        return JsonResponse({'name': name, 'id': id}, status=200)