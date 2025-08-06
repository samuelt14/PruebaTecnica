from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from actas_app.models import Acta, Compromiso
from django.utils.timezone import now
from pathlib import Path

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea o actualiza usuarios por defecto y genera actas de prueba con compromisos'

    def handle(self, *args, **options):

        admin = self.create_or_update_user(
            username='admin',
            email='admin@ejemplo.com',
            password='admin123',
            role='admin'
        )

        base = self.create_or_update_user(
            username='base',
            email='base@ejemplo.com',
            password='base123',
            role='base'
        )


        pdf_path = Path('media/actas_pdfs')
        pdf_path.mkdir(parents=True, exist_ok=True)
        sample_pdf = pdf_path / 'acta_demo.pdf'
        if not sample_pdf.exists():
            with open(sample_pdf, 'wb') as f:
                f.write(b'%PDF-1.4\n%Demo PDF para actas\n')

        acta1, _ = Acta.objects.get_or_create(
            title="Acta General",
            defaults={'status': 'Abierta', 'date': now().date(), 'created_by': admin, 'pdf': 'actas_pdfs/acta_demo.pdf'}
        )

        acta2, _ = Acta.objects.get_or_create(
            title="Acta Proyecto",
            defaults={'status': 'Cerrada', 'date': now().date(), 'created_by': base, 'pdf': 'actas_pdfs/acta_demo.pdf'}
        )

        Compromiso.objects.get_or_create(
            acta=acta1,
            description="Compromiso asignado a admin",
            responsible=admin
        )

        Compromiso.objects.get_or_create(
            acta=acta2,
            description="Compromiso asignado a base",
            responsible=base
        )

        self.stdout.write(self.style.SUCCESS('Actas y compromisos creados para admin y base'))

    def create_or_update_user(self, username, email, password, role):
        user, created = User.objects.get_or_create(username=username)
        user.email = email
        user.role = role
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Usuario {username} creado'))
        else:
            self.stdout.write(self.style.WARNING(f'Usuario {username} actualizado'))

        self.stdout.write(f'    → Email: {email} | Password: {password}')
        return user
