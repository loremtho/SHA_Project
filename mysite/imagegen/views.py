from django.shortcuts import render
from diffusers import StableDiffusionPipeline
import torch

# Stable Diffusion 모델 로드
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def generate_image(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        if prompt:
            # 이미지 생성
            image = pipe(prompt).images[0]
            image.save("media/generated_image.png")  # 이미지를 파일로 저장

    return render(request, "imagegen/generate_image.html")
