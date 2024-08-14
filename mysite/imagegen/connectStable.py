# from diffusers import DiffusionPipeline
from diffusers import FluxPipeline
from django.conf import settings
import torch
from datetime import datetime
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "true"

def createIMG(prompt_text):
    # 모델 로드
    
    from huggingface_hub import login
    huggingface_token = "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"
    login(token=huggingface_token)
    
    model_id = "black-forest-labs/FLUX.1-dev"
    pipe = FluxPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe.load_lora_weights("XLabs-AI/flux-RealismLora")
    pipe = pipe.to("cuda")  # GPU 사용
    
    pipe.enable_xformers_memory_efficient_attention()


    # 세부 설정
    prompt = prompt_text
    num_inference_steps = 100  # 생성 단계 수
    guidance_scale = 7  # CFG 스케일


    # 이미지 생성
    image = pipe(prompt, 
                num_inference_steps=num_inference_steps, 
                guidance_scale=guidance_scale,
                height=512,
                width=512).images[0]
    

    #이미지 저장 세부 설정
    image_save_folder = os.path.join(settings.MEDIA_ROOT, 'picture')
    os.makedirs(image_save_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_filename = f"{timestamp}.png"
    image_path = os.path.join(image_save_folder, image_filename)

    # 이미지 저장
    image.save(image_path)
    return f'media/picture/{image_filename}'  # 저장된 이미지의 경로
