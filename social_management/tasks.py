# social_management/tasks.py
from celery import shared_task
from django.utils import timezone
import requests

@shared_task
def publicar_posts_programados():
    from .models import Post
    # Obtener la fecha y hora actual
    ahora = timezone.now()
    
    # Filtrar los posts programados para la fecha y hora actuales
    posts_para_publicar = Post.objects.filter(
        estado='P',  # Estado Programado
        programmed_post_time__lte=ahora  # Fecha/hora programada para publicar
    )

    for post in posts_para_publicar:
        try:
            # Llamada a la API del frontend para publicar el post
            response = requests.post("FRONTEND_API_URL", json={'contenido': post.contenido})

            if response.status_code == 200:
                # Si la publicación fue exitosa, actualizar el estado del post a 'Publicado'
                post.estado = 'Pu'
                post.link = response.json().get('link')  # Asumimos que el link del post está en la respuesta
                post.save()
            else:
                # Si falla, actualizar el estado del post a 'Fallido'
                post.estado = 'F'
                post.save()
        except Exception as e:
            # Si hay algún error, marcar el post como 'Fallido'
            post.estado = 'F'
            post.save()
            print(f"Error publicando el post {post.id}: {e}")

@shared_task
def imprimir_mensaje_prueba():
    print("Probando - Tarea ejecutada exitosamente")