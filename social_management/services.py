import requests
import boto3
from botocore.exceptions import NoCredentialsError
from smmproject import settings 
import requests
from datetime import timedelta
from django.utils.timezone import now

from decouple import config 

def obtener_url_s3(nombre_archivo):
    # Crear cliente S3 utilizando las credenciales proporcionadas
    s3 = boto3.client('s3', 
                      region_name=settings.AWS_S3_REGION_NAME,
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    try:
        # Generar una URL pre-firmada para acceder al archivo en S3
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': nombre_archivo},
                                        ExpiresIn=3600)  # URL válida por 1 hora
        return url
    except NoCredentialsError:
        print("Credenciales de AWS no disponibles o incorrectas")
        return None
    except Exception as e:
        print(f"Error generando URL pre-firmada: {e}")
        return None


def publicar_video_tiktok(access_token, nombre_archivo_s3):
    # Obtener la URL pre-firmada del archivo en S3
    video_url = obtener_url_s3(nombre_archivo_s3)
    if not video_url:
        return {"error": "No se pudo obtener el URL del archivo en S3"}

    # Endpoint de la API de TikTok para publicar videos
    tiktok_api_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
    
    # Encabezados de la solicitud con el token de acceso
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Cuerpo de la solicitud con la información del video
    data = {
        "source_info": {
            "source": "PULL_FROM_URL",
            "video_url": video_url  # Usamos el URL generado desde S3
        }
    }

    try:
        # Realizar la solicitud POST a la API de TikTok
        response = requests.post(tiktok_api_url, json=data, headers=headers)
        if response.status_code == 200:
            # Si la solicitud fue exitosa, devolver los datos de la respuesta
            return response.json()
        else:
            # En caso de error, imprimir el código y el mensaje de error
            print(f"Error al publicar video en TikTok: {response.status_code} - {response.text}")
            return {"error": f"Error en TikTok: {response.status_code} - {response.text}"}
    except Exception as e:
        # Capturar cualquier otra excepción que ocurra
        print(f"Error en la solicitud a TikTok: {e}")
        return {"error": f"Excepción: {str(e)}"}

def renovar_token_largo_duracion(cuenta):
    try:
        url = "https://graph.facebook.com/v12.0/oauth/access_token"
        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': config('FACEBOOK_APP_ID'),
            'client_secret': config('FACEBOOK_APP_SECRET'),
            'fb_exchange_token': cuenta.token_autenticacion,
        }
        response = requests.get(url, params=params)
        response_data = response.json()

        if 'access_token' in response_data:
            cuenta.token_autenticacion = response_data['access_token']
            cuenta.fecha_expiracion_token = now() + timedelta(days=60)
            cuenta.save()
            return True
        else:
            raise Exception(f"Error al renovar el token: {response_data.get('error', 'Desconocido')}")
    except Exception as e:
        print(f"Error al renovar el token: {str(e)}")
        return False

def verificar_y_renovar_token(cuenta):
    # Verifica si el token está por expirar y lo renueva si es necesario.
    if cuenta.fecha_expiracion_token <= now() + timedelta(days=1):  # Comparación usando `now()`
        if not renovar_token_largo_duracion(cuenta):
            raise Exception("No se pudo renovar el token de larga duración.")