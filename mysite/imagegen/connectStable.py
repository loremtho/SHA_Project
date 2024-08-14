from diffusers import StableDiffusionPipeline, LMSDiscreteScheduler
from django.conf import settings
import torch
from datetime import datetime
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "true"

def createIMG(prompt_text):
    # 모델 로드
    model_id = "Linaqruf/anything-v3.0"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")  # GPU 사용
    
    pipe.enable_xformers_memory_efficient_attention()

    # 스케줄러 설정 (LMSDiscreteScheduler 사용)
    # pipe.scheduler = LMSDiscreteScheduler(
    #     beta_start=0.00085,
    #     beta_end=0.012,
    #     beta_schedule="scaled_linear"
    # )
    
    # 해상도 및 품질 개선 옵션 설정
    hires_fix = {
    "upscaler": "R-ESRGAN 4x+",  # 해상도 업스케일러 설정
    "hires_steps": 50,  # Hires steps 설정
    "denoising_strength": 0.5,  # 노이즈 제거 강도 설정
    "upscale_by": 2,  # 이미지 크기 2배로 설정
    "resize_width": 512,  # 너비 설정
    "resize_height": 512  # 높이 설정
    }

    # 세부 설정
    prompt = prompt_text
    num_inference_steps = 100  # 생성 단계 수
    guidance_scale = 7  # CFG 스케일


    # 이미지 생성
    image = pipe(prompt, 
                num_inference_steps=hires_fix["hires_steps"], 
                guidance_scale=guidance_scale,
                denoising_strength=hires_fix["denoising_strength"]).images[0]
    
    
    # 이미지 크기 조정
    image = image.resize((hires_fix["resize_width"], hires_fix["resize_height"]))

    #이미지 저장 세부 설정
    image_save_folder = os.path.join(settings.MEDIA_ROOT, 'picture')
    os.makedirs(image_save_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_filename = f"{timestamp}.png"
    image_path = os.path.join(image_save_folder, image_filename)

    # 이미지 저장
    image.save(image_path)
    return f'media/picture/{image_filename}'  # 저장된 이미지의 경로
