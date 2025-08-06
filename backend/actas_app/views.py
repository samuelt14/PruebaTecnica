# backend/actas_app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.http import FileResponse, Http404
from django.conf import settings
from django.db import models
import os

from .models import Acta, Gestion
from .serializers import ActaSerializer, GestionSerializer

User = get_user_model()


class CustomAuthToken(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Correo y contraseña son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'role':  user.get_role_display()  # ✅ muestra "Usuario" o "Administrador"
        })


class ActaList(generics.ListAPIView):
    serializer_class = ActaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Acta.objects.all() if user.role == 'admin' else Acta.objects.filter(
            models.Q(created_by=user) | models.Q(compromisos__responsible=user)
        ).distinct()

        # ✅ Filtros opcionales
        title       = self.request.query_params.get('title')
        status_param = self.request.query_params.get('status')
        date        = self.request.query_params.get('date')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if status_param:
            queryset = queryset.filter(status__icontains=status_param)
        if date:
            queryset = queryset.filter(date=date)

        return queryset


class ActaDetail(generics.RetrieveAPIView):
    serializer_class = ActaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Acta.objects.all()
        return Acta.objects.filter(
            models.Q(created_by=user) | models.Q(compromisos__responsible=user)
        ).distinct()


class GestionCreate(generics.CreateAPIView):
    serializer_class = GestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        compromiso = serializer.validated_data['compromiso']
        user = self.request.user
        if user.role != 'admin' and compromiso.responsible != user:
            raise PermissionDenied("No puedes agregar gestión a este compromiso")
        serializer.save()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def protected_media(request, path):
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(full_path):
        raise Http404("Archivo no encontrado")
    return FileResponse(open(full_path, 'rb'))
