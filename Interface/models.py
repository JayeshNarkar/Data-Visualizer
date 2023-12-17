from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    user_info = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='static/profile_pics/', blank=True, null=True)

    def serialize(self):
        default_profile_picture_url = 'static/profile_pics/default.jpg'        
        return {
            "id": self.id,
            "username": self.username,
            "profile_picture": self.profile_picture.url if self.profile_picture else default_profile_picture_url,
            "user_info": self.user_info
        }
    
class Data(models.Model):
    is_active = models.BooleanField(default=False)
    file_field = models.FileField(upload_to='static/csv_files/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    date_index = models.IntegerField(null=True, blank=True, default=0)
    dataset_index = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return f"{self.name}"



