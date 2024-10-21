# social_management/services.py
import requests
import boto3
from botocore.exceptions import NoCredentialsError

S3_BUCKET = 's3-dp2-villaizan-redes'
S3_REGION = 'us-east-1'

def obtener_url_s3(nombre_archivo):
    # Al no proporcionar aws_access_key_id y aws_secret_access_key, se usarán las credenciales del rol IAM asociado
    s3 = boto3.client('s3', region_name=S3_REGION)

    try:
        # Generar una URL pre-firmada para el archivo en S3
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': S3_BUCKET, 'Key': nombre_archivo},
                                        ExpiresIn=3600)  # URL válida por 1 hora
        return url
    except NoCredentialsError:
        print("Credenciales no disponibles")
        return None


def publicar_video_tiktok(access_token, nombre_archivo_s3):
    video_url = obtener_url_s3(nombre_archivo_s3)
    if not video_url:
        return {"error": "No se pudo obtener el URL del archivo en S3"}

    tiktok_api_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "source_info": {
            "source": "PULL_FROM_URL",
            "video_url": video_url  # Usamos el URL generado de S3
        }
    }

    try:
        response = requests.post(tiktok_api_url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al publicar video en TikTok: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error en la solicitud a TikTok: {e}")
        return None
