from django.urls import path
from .views import CustomAuthToken, ActaList, ActaDetail, GestionCreate

urlpatterns = [
    # Login y obtención de token + rol
    path('login/', CustomAuthToken.as_view(), name='login'),
    # Listar y filtrar actas
    path('actas/', ActaList.as_view(), name='acta-list'),
    # Detalle de una acta
    path('actas/<int:pk>/', ActaDetail.as_view(), name='acta-detail'),
    # Crear gestión para un compromiso
    path('gestiones/', GestionCreate.as_view(), name='gestion-create'),
]
    