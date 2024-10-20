import requests
import boto3
from botocore.exceptions import NoCredentialsError

# Información del bucket S3 y la región
S3_BUCKET = 's3-dp2-villaizan-redes'
S3_REGION = 'us-east-1'

# Tus credenciales de AWS (accesos ya proporcionados)
AWS_ACCESS_KEY = 'ASIAR3IZ5TJHRN766ECK'  # Reemplaza con tu access key
AWS_SECRET_KEY = 'qJs0wP5RKSA/IVcyqZperXS8p3SmzTfWnpNzS4ZT'  # Reemplaza con tu secret key


def obtener_url_s3(nombre_archivo):
    # Crear cliente S3 utilizando las credenciales proporcionadas
    s3 = boto3.client('s3', 
                      region_name=S3_REGION,
                      aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY)

    try:
        # Generar una URL pre-firmada para acceder al archivo en S3
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': S3_BUCKET, 'Key': nombre_archivo},
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
