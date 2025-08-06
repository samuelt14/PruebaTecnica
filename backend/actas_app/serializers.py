from rest_framework import serializers
from .models import User, Acta, Compromiso, Gestion
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role_display')  

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'role']


class CompromisoSerializer(serializers.ModelSerializer):
    responsible = UserSerializer(read_only=True)

    class Meta:
        model  = Compromiso
        fields = ['id', 'description', 'responsible']


class ActaSerializer(serializers.ModelSerializer):
    compromisos = CompromisoSerializer(many=True, read_only=True)
    created_by  = UserSerializer(read_only=True)

    class Meta:
        model  = Acta
        fields = ['id', 'title', 'status', 'date', 'created_by', 'pdf', 'compromisos']


class GestionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Gestion
        fields = ['id', 'compromiso', 'date', 'description', 'attachment']

class GestionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Gestion
        fields = ['id', 'compromiso', 'date', 'description', 'attachment']

    def validate_attachment(self, file):
        if file.content_type not in ('application/pdf', 'image/jpeg'):
            raise serializers.ValidationError('Sólo PDF o JPG.')
        if file.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Máximo 5 MB.')
        return file