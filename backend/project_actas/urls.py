from django.contrib import admin
from django.urls import path, include
from actas_app.views import protected_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('actas_app.urls')),
    path('media/<path:path>/', protected_media, name='protected-media'),
]
