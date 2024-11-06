# surveys/tasks.py
from celery import shared_task
from django.utils import timezone
import requests
import pytz

@shared_task
def manejar_encuestas_vencidas():
    from .models import Encuesta

    # Obtener la fecha y hora actual en America/Lima
    lima = pytz.timezone('America/Lima')
    ahora = timezone.now().astimezone(lima).date()  # Convertir a fecha en Lima

    # Filtrar las encuestas cuya fecha de finalización ha pasado y que aún están activas
    encuestas_vencidas = Encuesta.objects.filter(
        end_date__lt=ahora,  # Fecha de finalización menor a la fecha actual
        status__in=['Activa']  # Encuestas que aún están activas
    )

    for encuesta in encuestas_vencidas:
        try:
            # Llamada a la API del frontend para cerrar o eliminar la encuesta
            response = requests.post("https://helado-villaizan.vercel.app/api/encuestas/desactivar", json={'encuesta_id': encuesta.id})

            if response.status_code == 200:
                # Si la acción fue exitosa, actualiza el estado de la encuesta a "Cerrada"
                encuesta.status = 'Cerrada'
                encuesta.save()
            else:
                # Si falla la llamada, puedes registrar un error (opcional)
                print(f"Error al cerrar la encuesta {encuesta.id}: {response.status_code}")
        except Exception as e:
            print(f"Error procesando la encuesta {encuesta.id}: {e}")
