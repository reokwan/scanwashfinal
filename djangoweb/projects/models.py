from django.contrib.auth.models import AbstractUser
from django.db import models

class CameraConfig(models.Model):
    camera1_url = models.CharField(max_length=255, default='')
    camera2_url = models.CharField(max_length=255, default='')
    camera3_url = models.CharField(max_length=255, default='')

class CustomUser(AbstractUser):
    rut = models.CharField(max_length=10, unique=True)
    is_employee = models.BooleanField(default=False)
    camera_config = models.OneToOneField(CameraConfig, on_delete=models.SET_NULL, null=True, blank=True)

class CarPlates(models.Model):
    plate_number = models.CharField(max_length=10, unique=True)
    date_time = models.DateTimeField(auto_now_add=True)
    image_path = models.CharField(max_length=100)
    car_year = models.IntegerField()
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    car_type = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
