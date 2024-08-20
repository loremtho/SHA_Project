# from diffusers import DiffusionPipeline
# from diffusers import FluxPipeline
from diffusers import StableDiffusion3Pipeline
from diffusers import StableDiffusionPipeline
from diffusers import DiffusionPipeline
from django.conf import settings
import torch
from datetime import datetime
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "true"

def createIMG(prompt_text, model_id, num_inference_steps, guidance_scale):
    # 모델 로드
    
    from huggingface_hub import login
    huggingface_token = "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"
    login(token=huggingface_token)
    
    if model_id == "stabilityai/stable-diffusion-3-medium-diffusers":
        pipe = StableDiffusion3Pipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    elif model_id == "eienmojiki/Anything-XL":
        pipe = DiffusionPipeline.from_pretrained("eienmojiki/Anything-XL")
        
    pipe = DiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to("cuda")  # GPU 사용
    
    prompt = prompt_text
    
    pipe.enable_xformers_memory_efficient_attention()

    

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
    print('model id = ' + model_id)
    print('num_inference_steps = ' + str(num_inference_steps))
    print('guidance_scale = ' + str(guidance_scale))
    return f'media/picture/{image_filename}'  # 저장된 이미지의 경로
    
