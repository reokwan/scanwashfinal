from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, CarPlates, CameraConfig

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'rut')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'rut')

class CameraConfigForm(forms.ModelForm):
    class Meta:
        model = CameraConfig
        fields = ('camera1_url', 'camera2_url', 'camera3_url')
