from django.shortcuts import render, redirect
from django.contrib import messages
import os
import base64
import mysql.connector
from .geminiAPI import translate_to_english, transform_to_stable_diffusion_prompt
from .connectStable import createIMG
from django.conf import settings

# 전역 변수
is_logged_in = False
logged_in_user = None
logged_in_username = None

# MySQL 데이터베이스 설정
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'my_database'
}

# 이미지 생성 뷰
def image_generate_view(request):
    global is_logged_in, logged_in_user, logged_in_username
    
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
        createIMG(pos_prompt, neg_prompt, model_id, num_inference_steps, guidance_scale, is_logged_in, logged_in_user)

        # 이미지 경로 설정
        image_folder = 'media/picture/'
        image_filename = sorted(os.listdir(image_folder))[-1]  # 가장 최근 생성된 이미지 선택
        image_url = os.path.join(image_folder, image_filename)

        # 세션에 이미지 URL 저장
        request.session['image_url'] = image_url

        print(image_url)
        # 이미지 생성 후 리디렉션
        return redirect('generate_image')

    return render(request, 'imagegen/generate3.html', {
        'is_logged_in': is_logged_in,
        'logged_in_user': logged_in_user,
        'logged_in_username': logged_in_username
    })

# 로그인 뷰
def login_view(request):
    global is_logged_in, logged_in_user, logged_in_username

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
                return redirect('generate_image')  # 로그인 후 generate_image 화면으로 리디렉션
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
    global is_logged_in, logged_in_user, logged_in_username

    is_logged_in = False
    logged_in_user = None
    logged_in_username = None
    return redirect('generate')  # 로그아웃 후 generate 화면으로 리디렉션

# 히스토리 뷰
def generate_image_view(request):
    if not is_logged_in:
        return 0  # 로그인하지 않은 경우 로그인 페이지로 리디렉션

    # 세션에서 이미지 URL 가져오기
    image_url = request.session.get('image_url')
    # 세션에서 URL을 제거
    if 'image_url' in request.session:
        del request.session['image_url']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 사용자 이미지 히스토리 쿼리
    cursor.execute("SELECT imgname FROM images WHERE user_id = %s", [logged_in_user])
    rows = cursor.fetchall()

    image_history = []
    for row in rows:
        image_filename = row[0]
        image_path = os.path.join('media/picture/', image_filename)
        if os.path.isfile(image_path):
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                encoded_image = base64.b64encode(image_data).decode('utf-8')
                image_src = f"data:image/png;base64,{encoded_image}"
                image_history.append(image_src)

    cursor.close()
    conn.close()
    
   # 이미지 URL을 MEDIA_URL을 포함한 경로로 설정
    if image_url:
        image_url = os.path.join(settings.MEDIA_URL, 'picture', os.path.basename(image_url))

    print(image_url)
    # 템플릿으로 데이터 전달
    return render(request, 'imagegen/generate3.html', {
        'image_url': image_url,
        'image_history': image_history,
        'is_logged_in': is_logged_in,
        'logged_in_user': logged_in_user,
        'logged_in_username': logged_in_username
    })
