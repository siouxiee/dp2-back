from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smmproject.settings')

app = Celery('smmproject')

# Cargar configuración desde Django settings, prefijadas por "CELERY"
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks de todos los apps registrados
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'publish-scheduled-posts': {
        'task': 'social_management.tasks.publicar_posts_programados',
        'schedule': crontab(minute='*/1'),  # Revisar cada minuto si hay publicaciones programadas
    },
    'manejar-encuestas-vencidas': {
        'task': 'surveys.tasks.manejar_encuestas_vencidas',
        'schedule': crontab(hour='*/1'),  # Se ejecuta cada hora
    },
}
