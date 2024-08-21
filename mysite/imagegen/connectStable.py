# from diffusers import DiffusionPipeline
# from diffusers import FluxPipeline
from diffusers import StableDiffusion3Pipeline
from diffusers import DiffusionPipeline, EulerAncestralDiscreteScheduler, DPMSolverMultistepScheduler, DPMSolverSDEScheduler
from django.conf import settings
import torch
from datetime import datetime
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "true"

def createIMG(pos_prompt, neg_prompt, model_id, num_inference_steps, guidance_scale):
    # 모델 로드
    
    from huggingface_hub import login
    huggingface_token = "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"
    login(token=huggingface_token)
    
    if model_id == "SG161222/Realistic_Vision_V6.0_B1_noVAE":
        pipe = DiffusionPipeline.from_pretrained(model_id)
        pipe.scheduler = DPMSolverSDEScheduler.from_config(pipe.scheduler.config)
    elif model_id == "eienmojiki/Anything-XL":
        pipe = DiffusionPipeline.from_pretrained(model_id)
        pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
        # pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        
    # pipe = pipe.to("cuda")  # GPU 사용
    pipe.enable_model_cpu_offload()
    
    pipe.enable_xformers_memory_efficient_attention()

    # 이미지 생성
    image = pipe(prompt=pos_prompt,
                negative_prompt=neg_prompt, 
                num_inference_steps=num_inference_steps, 
                guidance_scale=guidance_scale,
                height=768,
                width=512).images[0]
    

    #이미지 저장 세부 설정
    image_save_folder = os.path.join(settings.MEDIA_ROOT, 'picture')
    os.makedirs(image_save_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_filename = f"{timestamp}.png"
    image_path = os.path.join(image_save_folder, image_filename)

    # 이미지 저장
    image.save(image_path)
    print('model id = ' + model_id)
    print('num_inference_steps = ' + str(num_inference_steps))
    print('guidance_scale = ' + str(guidance_scale))
    print(image_path)
    print(f'media/picture/{image_filename}')
    return f'media/picture/{image_filename}'  # 저장된 이미지의 경로
    
