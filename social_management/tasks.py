# social_management/tasks.py
from celery import shared_task
from django.utils import timezone
import psycopg2
import pytz
import requests

# Configuración de la conexión a la base de datos
DB_HOST = 'ep-cold-hill-a4n65zi1-pooler.us-east-1.aws.neon.tech'
DB_NAME = 'verceldb'
DB_USER = 'default'
DB_PASSWORD = 'bOoyAur5eNa1'
DB_PORT = '5432'

@shared_task
def publicar_posts_programados():
    # Obtener la fecha y hora actual en America/Lima
    lima = pytz.timezone('America/Lima')
    ahora = timezone.now().astimezone(lima)

    # Convertir a GMT para comparar con los valores almacenados en la base de datos (que están en GMT)
    gmt = pytz.timezone('GMT')
    ahora_gmt = ahora.astimezone(gmt)

    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Consulta para obtener los posts programados excluyendo Facebook
        query = """
        SELECT posts.id, posts.type, posts.status, posts.thumbnail, posts.content, posts.post_time, social_media.platform
        FROM posts
        JOIN social_media ON posts.id = social_media.post_id
        WHERE posts.status = 'programado' AND posts.post_time <= %s AND social_media.platform NOT IN ('facebook');
        """
        cursor.execute(query, (ahora_gmt,))
        posts_para_publicar = cursor.fetchall()

        if posts_para_publicar:
            for post in posts_para_publicar:
                post_id, post_type, status, thumbnail, content, post_time, platform = post
                try:
                    # Preparar los datos para la API
                    post_data = {
                        "id": str(post_id),
                        "social_media": [platform.lower()],
                        "type": post_type.lower() if post_type else "video",
                        "status": "publicado",
                        "thumbnail": thumbnail,
                        "media": [thumbnail],  # Usar el mismo URL como placeholder de media
                        "content": content,
                        "post_time": post_time.isoformat()
                    }

                    # Determinar la URL de la API en función de la plataforma
                    api_url = f"https://helado-villaizan.vercel.app/api/{platform.lower()}/post"

                    # Llamada a la API del frontend para publicar el post
                    response = requests.post(api_url, json=post_data)

                    if response.status_code == 200:
                        print(f"Post {post_id} publicado exitosamente en {platform}.")

                        # Actualizar el estado del post a 'publicado'
                        update_query = "UPDATE posts SET status = 'publicado' WHERE id = %s;"
                        cursor.execute(update_query, (post_id,))
                        conn.commit()  # Confirmar los cambios en la base de datos
                    else:
                        print(f"Error publicando el post {post_id} en {platform}: {response.status_code} - {response.text}")
                        # No cambiar el estado a 'fallido', mantenerlo como 'programado'

                except Exception as e:
                    print(f"Error publicando el post {post_id}: {e}")
                    # No cambiar el estado a 'fallido', mantenerlo como 'programado'

        else:
            print("No hay posts programados para publicar.")

        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error al conectar o consultar la base de datos: {e}")


# @shared_task
# def renovar_tokens_facebook_instagram():
#     try:
#         # Llamada a la API para renovar los tokens de Facebook e Instagram
#         response = requests.post("https://helado-villaizan.vercel.app/api/meta/token-renew")

#         if response.status_code == 200:
#             # Si la renovación fue exitosa
#             print("Tokens renovados exitosamente.")
#         else:
#             # Si hubo un problema con la renovación
#             print(f"Error al renovar los tokens: {response.status_code} - {response.text}")
#     except Exception as e:
#         # Si ocurre algún error durante la solicitud
#         print(f"Error al intentar renovar los tokens: {e}")

# @shared_task
# def imprimir_mensaje_prueba():
#     print("Probando - Tarea ejecutada exitosamente")