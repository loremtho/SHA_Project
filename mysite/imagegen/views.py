from django.shortcuts import render
import os

# MySQL 데이터베이스 설정
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '0000',
    'database': 'my_database'
}

# 이미지 생성 뷰
def image_generate_view(request):
    image_url = None
    user_username = request.session.get('username')  # 로그인한 사용자의 이름 가져오기
    if request.method == "POST":
        # 기존 이미지 생성 로직
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
        
        return render(request, 'imagegen/generate3.html', {'image_url': image_url, 'username': user_username})

    return render(request, 'imagegen/generate3.html', {'username': user_username})
