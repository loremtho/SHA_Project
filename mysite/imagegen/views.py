from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .geminiAPI import translate_to_english, transform_to_stable_diffusion_prompt
from .connectStable import createIMG
import os

# 이미지 생성 뷰
def image_generate_view(request):
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
        
        return render(request, 'imagegen/generate3.html', {'image_url': image_url})

    return render(request, 'imagegen/generate3.html')

# 로그인 뷰
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('generate')  # 로그인 후 리디렉션할 URL
        else:
            messages.error(request, '로그인 정보를 확인해 주세요.')
    else:
        form = AuthenticationForm()
    return render(request, 'imagegen/login.html', {'form': form})

# 회원 가입 뷰
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '회원 가입이 완료되었습니다. 로그인 해 주세요.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'imagegen/signup.html', {'form': form})

