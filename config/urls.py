from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('course/', include('Ims.urls', namespace='course')),
    path('user/', include('users.urls', namespace='course')),
]
