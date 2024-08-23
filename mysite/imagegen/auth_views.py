from django.shortcuts import render, redirect
from django.contrib import messages
import mysql.connector

# MySQL 데이터베이스 설정
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '0000',
    'database': 'my_database'
}

# 로그인 뷰
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 데이터베이스 연결
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        try:
            # 쿼리 작성
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            values = (username, password)
            cursor.execute(query, values)
            user = cursor.fetchone()

            if user:
                # 로그인 처리
                request.session['user_id'] = user[0]  # user_id를 세션에 저장
                request.session['username'] = username
                return redirect('generate')  # 로그인 후 리디렉션할 URL
            else:
                messages.error(request, '사용자 이름이나 비밀번호가 잘못되었습니다.')
        except mysql.connector.Error as err:
            messages.error(request, f"오류 발생: {err}")
        finally:
            cursor.close()
            conn.close()
    return render(request, 'imagegen/login.html')

# 회원 가입 뷰
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 데이터베이스 연결
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 쿼리 작성
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        values = (username, email, password)

        try:
            cursor.execute(query, values)
            conn.commit()
            messages.success(request, '회원 가입이 완료되었습니다. 로그인 해 주세요.')
            return redirect('login')
        except mysql.connector.Error as err:
            messages.error(request, f"오류 발생: {err}")
        finally:
            cursor.close()
            conn.close()
    return render(request, 'imagegen/signup.html')

# 로그아웃 뷰
def logout_view(request):
    request.session.flush()  # 세션 초기화
    return redirect('generate')  # 로그아웃 후 리디렉션할 URL
