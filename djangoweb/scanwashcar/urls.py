from django.contrib import admin
from django.urls import path
from projects import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout , name='logout'),
    path('signin/', views.signin, name='signin'),
    path('employee/', views.employee, name='employee'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('start_detection/', views.start_detection_view, name='start_detection'),
    path('stop_detection/', views.stop_detection_view, name='stop_detection'),
    path('detect_plate/', views.detect_plate, name='detect_plate'),
    path('create_user/', views.create_user, name='create_user'),
    path('user_profiel/', views.user_profile, name='user_profile'),
    path('camera_config/', views.camera_config, name='camera_config'),
    path('update_user/', views.update_user, name='update_user'),
] 



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
