from django.db import models
from django.conf import settings

class Image(models.Model):
    user_id = models.IntegerField()  # 유저 ID 저장
    imgname = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.imgname

    def get_image_url(self):
        return f"{settings.MEDIA_URL}picture/{self.imgname}"