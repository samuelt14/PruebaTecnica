from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('base',  'Usuario'),      
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='base')

class Acta(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='actas_pdfs/')

    def __str__(self):
        return f"{self.title} ({self.status})"

class Compromiso(models.Model):
    acta = models.ForeignKey(Acta, related_name='compromisos', on_delete=models.CASCADE)
    description = models.TextField()
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Compromiso #{self.id} en {self.acta.title}"

class Gestion(models.Model):
    compromiso = models.ForeignKey(Compromiso, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    attachment = models.FileField(upload_to='gestiones/')

    def __str__(self):
        return f"Gestión #{self.id} para {self.compromiso}"
    