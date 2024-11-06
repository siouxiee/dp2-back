# social_management/tasks.py
from celery import shared_task
from django.utils import timezone
import requests
import pytz

@shared_task
def publicar_posts_programados():
    from .models import Post
    # Obtener la fecha y hora actual en America/Lima
    lima = pytz.timezone('America/Lima')
    ahora = timezone.now().astimezone(lima)

    # Convertir a GMT para comparar con los valores almacenados en la base de datos (que están en GMT)
    gmt = pytz.timezone('GMT')
    ahora_gmt = ahora.astimezone(gmt)

    # Filtrar los posts programados para la fecha y hora actuales en GMT
    posts_para_publicar = Post.objects.filter(
        estado='P',  # Estado Programado
        programmed_post_time__lte=ahora_gmt  # Fecha/hora programada para publicar
    )

    for post in posts_para_publicar:
        try:
            # Preparar los datos para la API
            post_data = {
                "id": str(post.id),  # Convertir UUID a string
                "social_media": [post.red_social.lower()],  # Convertir a minúsculas para el API
                "type": post.tipo.lower() if post.tipo else "video",  # Usar tipo si está definido, por defecto 'video'
                "status": "publicado",
                "thumbnail": post.preview,  # Usar la URL del preview si está disponible
                "media": [post.media],  # Usar URL del contenido multimedia
                "content": post.contenido,  # Contenido del post
                "post_time": post.programmed_post_time.isoformat()  # Convertir a ISO formato
            }

            # Llamada a la API del frontend para publicar el post
            response = requests.post("https://helado-villaizan.vercel.app/api/facebook/post", json=post_data)

            if response.status_code == 200:
                # Si la publicación fue exitosa, actualizar el estado del post a 'Publicado'
                post.estado = 'Pu'
                post.link = response.json().get('link')  # Asumimos que el link del post está en la respuesta
                post.save()
            else:
                # Si falla, actualizar el estado del post a 'Fallido'
                post.estado = 'F'
                post.save()
                print(f"Error publicando el post {post.id}: {response.status_code} - {response.text}")
        except Exception as e:
            # Si hay algún error, marcar el post como 'Fallido'
            post.estado = 'F'
            post.save()
            print(f"Error publicando el post {post.id}: {e}")

@shared_task
def renovar_tokens_facebook_instagram():
    try:
        # Llamada a la API para renovar los tokens de Facebook e Instagram
        response = requests.post("https://helado-villaizan.vercel.app/api/meta/token-renew")

        if response.status_code == 200:
            # Si la renovación fue exitosa
            print("Tokens renovados exitosamente.")
        else:
            # Si hubo un problema con la renovación
            print(f"Error al renovar los tokens: {response.status_code} - {response.text}")
    except Exception as e:
        # Si ocurre algún error durante la solicitud
        print(f"Error al intentar renovar los tokens: {e}")

@shared_task
def imprimir_mensaje_prueba():
    print("Probando - Tarea ejecutada exitosamente")