from django.db import models
import uuid

# Create your models here.

class CuentaRedSocial(models.Model):
    red_social = models.CharField(max_length=50)

    usuario = models.CharField(max_length=100)  # Nombre de usuario en la red social
    open_id = models.CharField(max_length=255, null=True, blank=True)  # ID único (TikTok, Facebook)

    page_id = models.CharField(max_length=255, blank=True, null=True)  # ID de la página de Facebook
    instagram_business_account = models.CharField(max_length=255, blank=True, null=True)  # IG Business Account ID

    # Gestión de tokens
    token_autenticacion = models.TextField()  # Access Token
    refresh_token = models.TextField(blank=True, null=True)  # Refresh Token
    tipo_autenticacion = models.CharField(max_length=50, default='Bearer')  # OAuth2, Bearer, etc.

    # Fechas de vencimiento de los tokens
    fecha_expiracion_token = models.DateTimeField()  # Expiración del Access Token
    fecha_expiracion_refresh = models.DateTimeField(blank=True, null=True)  # Expiración del Refresh Token

    linked = models.BooleanField(default=False)  # Estado de vinculación

    class Meta:
        db_table = 'vi_cuentaredsocial'

    def __str__(self):
        return f"{self.usuario} en {self.red_social.nombre}"


class ReporteRedes(models.Model):
    cuenta_red_social = models.ForeignKey(CuentaRedSocial, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_usuarios = models.IntegerField()
    total_publicaciones = models.IntegerField()
    total_interacciones = models.IntegerField()

    class Meta:
        db_table = 'vi_reporteredes'  # Prefijo 'vi_' para la tabla

    def __str__(self):
        return f"Reporte del {self.fecha_inicio} al {self.fecha_fin}"


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ID como UUID
    cuenta = models.ForeignKey(
        'CuentaRedSocial',
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,  # Permitir nulo para borradores
        blank=True
    )
    contenido = models.TextField()
    link = models.URLField(null=True, blank=True)  # URL del post
    preview = models.URLField(null=True, blank=True)  # Thumbnail del contenido
    media = models.URLField(null=True, blank=True)  # URL del contenido multimedia

    fecha_publicacion = models.DateField(null=True, blank=True)  # Fecha de publicación
    fecha_creacion = models.DateField(auto_now_add=True)  # Fecha de creación
    programmed_post_time = models.DateTimeField(null=True, blank=True)  # Fecha programada para publicación

    ESTADO_CHOICES = [
        ('B', 'Borrador'),
        ('P', 'Programado'),
        ('Pu', 'Publicado'),
        ('F', 'Fallido'),
    ]
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)  # Estado del post

    RED_CHOICES = [
        ('TikTok', 'TikTok'),
        ('Facebook', 'Facebook'),
        ('Instagram', 'Instagram'),
    ]
    red_social = models.CharField(max_length=255, choices=RED_CHOICES, blank=True, null=True)  # Red social

    tipo = models.CharField(max_length=255, null=True, blank=True)  # Tipo de contenido (video/imagen)

    class Meta:
        db_table = 'vi_post'

    def __str__(self):
        return self.contenido[:50] if self.contenido else "Post sin contenido"



class Interaccion(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='interacciones')
    cuenta = models.ForeignKey(CuentaRedSocial, on_delete=models.CASCADE, related_name='interacciones')
    TIPO_CHOICES = [
        ('C', 'Comentario'),
        ('M', 'Mención'),
        ('D', 'Mensaje Directo'),
    ]
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    contenido = models.TextField()
    fecha = models.DateField()
    username = models.CharField(max_length=100)
    id_interaccion_red_social = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'vi_interaccion'  # Prefijo 'vi_' para la tabla

    def __str__(self):
        return f"{self.tipo} de {self.username}"


class Segmento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    criterio = models.TextField()
    fecha_creacion = models.DateField()
    cuenta = models.ForeignKey(CuentaRedSocial, on_delete=models.CASCADE, related_name='segmentos')

    class Meta:
        db_table = 'vi_segmento'  # Prefijo 'vi_' para la tabla

    def __str__(self):
        return self.nombre


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
       db_table = 'vi_etiqueta'  # Prefijo 'vi_' para la tabla

    def __str__(self):
        return self.nombre


class PostEtiqueta(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)

    class Meta:
        db_table = 'vi_postetiqueta'  # Prefijo 'vi_' para la tabla

    def __str__(self):
        return f"Etiqueta: {self.etiqueta.nombre} en Post: {self.post.contenido[:30]}"
