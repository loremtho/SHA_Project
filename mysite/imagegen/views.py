from django.shortcuts import render
from django.http import HttpResponse
from .geminiAPI import translate_to_english, transform_to_stable_diffusion_prompt
from .connectStable import createIMG
import os

def image_generate_view(request):
    image_url = None
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        negative_prompt = request.POST.get("negative_prompt", "")
        model_id = request.POST.get('model_id')
        num_inference_steps = int(request.POST.get('num_inference_steps'))
        guidance_scale = float(request.POST.get('guidance_scale'))
        neg_text = request.POST.get('neg_text')

        # 한글 설명을 영어로 번역
        english_text = translate_to_english(prompt)
        if negative_prompt:
            negative_english_text = translate_to_english(negative_prompt)
            negative_english_text = negative_prompt
            # 만약 모델 별 전용 부정 프롬프트가 있다면
            if neg_text:
                # 부정 프롬프트에 추가해줌
                negative_english_text = translate_to_english(negative_prompt + neg_text)
        else:
            negative_english_text = neg_text

        # Stable Diffusion 프롬프트로 변환
        prompt_text= transform_to_stable_diffusion_prompt(english_text, negative_english_text)
        
        print(negative_english_text)

        # 이미지 생성
        # createIMG(prompt_text)
        
        image_url = createIMG(prompt_text, model_id, num_inference_steps, guidance_scale)

        # 이미지 경로 설정
        image_folder = 'media/picture/'
        image_filename = sorted(os.listdir(image_folder))[-1]  # 가장 최근 생성된 이미지 선택
        image_url = os.path.join(image_folder, image_filename)
        
        return render(request, 'imagegen/generate.html', {'image_url': image_url})

    return render(request, 'imagegen/generate.html')
