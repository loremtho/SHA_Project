from django.shortcuts import render, redirect
from django.contrib import messages
import mysql.connector
from .geminiAPI import translate_to_english, transform_to_stable_diffusion_prompt
from .connectStable import createIMG
import os

# 전역 변수
is_logged_in = False
logged_in_user = None
logged_in_username = None  # 새로 추가된 전역 변수

# MySQL 데이터베이스 설정
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'my_database'
}

# 이미지 생성 뷰
def image_generate_view(request):
    global is_logged_in, logged_in_user, logged_in_username  # 전역 변수 사용 선언
    
    image_url = None
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        negative_prompt = request.POST.get("negative_prompt", "")
        model_id = request.POST.get('model_id')
        num_inference_steps = int(request.POST.get('num_inference_steps'))
        guidance_scale = float(request.POST.get('guidance_scale'))
        neg_text = request.POST.get('neg_text', "")
        pos_text = request.POST.get('pos_text', "")

        # 한글 설명을 영어로 번역
        english_text = translate_to_english(prompt)
        english_text += " " + str(pos_text)  # pos_text 추가
        
        if negative_prompt:
            negative_english_text = translate_to_english(negative_prompt)
            if neg_text:
                negative_english_text += " " + str(neg_text)  # neg_text 추가
        else:
            negative_english_text = str(neg_text)

        # Stable Diffusion 프롬프트로 변환
        pos_prompt, neg_prompt = transform_to_stable_diffusion_prompt(english_text, negative_english_text)
        
        print("긍정 프롬프트: " + str(pos_prompt))
        print("부정 프롬프트: " + str(neg_prompt))

        # 이미지 생성
        image_url = createIMG(pos_prompt, neg_prompt, model_id, num_inference_steps, guidance_scale)

        # 이미지 경로 설정
        image_folder = 'media/picture/'
        image_filename = sorted(os.listdir(image_folder))[-1]  # 가장 최근 생성된 이미지 선택
        image_url = os.path.join(image_folder, image_filename)
        
        return render(request, 'imagegen/generate3.html', {
            'image_url': image_url,
            'is_logged_in': is_logged_in,
            'logged_in_user': logged_in_user,
            'logged_in_username': logged_in_username
        })

    return render(request, 'imagegen/generate3.html', {
        'is_logged_in': is_logged_in,
        'logged_in_user': logged_in_user,
        'logged_in_username': logged_in_username
    })

# 로그인 뷰
def login_view(request):
    global is_logged_in, logged_in_user, logged_in_username  # 전역 변수 사용 선언

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 데이터베이스 연결
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        try:
            # 쿼리 작성
            query = "SELECT id, username FROM users WHERE username = %s AND password = %s"
            values = (username, password)
            cursor.execute(query, values)
            user = cursor.fetchone()
            
            if user:
                # 로그인 성공 시 전역 변수 수정
                is_logged_in = True
                logged_in_user = user[0]  # user[0]이 user_id
                logged_in_username = user[1]  # user[1]이 username
                print(logged_in_username)
                return redirect('generate')  # 로그인 후 generate 화면으로 리디렉션
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
    global is_logged_in, logged_in_user, logged_in_username  # 전역 변수 사용 선언

    is_logged_in = False
    logged_in_user = None
    logged_in_username = None
    return redirect('generate')  # 로그아웃 후 generate 화면으로 리디렉션
