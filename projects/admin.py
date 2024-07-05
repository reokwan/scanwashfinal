from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CarPlates, CameraConfig

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_employee']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rut', 'is_employee')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CarPlates)
admin.site.register(CameraConfig)