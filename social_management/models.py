from django.db import models

class RedSocial(models.Model):
    nombre = models.CharField(max_length=100)
    limite_caracteres = models.IntegerField()
    api_url = models.URLField()
    api_version = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'vi_redsocial'

    def __str__(self):
        return self.nombre


class CuentaRedSocial(models.Model):
    red_social = models.ForeignKey(RedSocial, on_delete=models.CASCADE)

    usuario = models.CharField(max_length=100)
    open_id = models.CharField(max_length=255, null=True, blank=True)

    page_id = models.CharField(max_length=255, blank=True, null=True)
    instagram_business_account = models.CharField(max_length=255, blank=True, null=True)

    # Gestión de tokens
    token_autenticacion = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    tipo_autenticacion = models.CharField(max_length=50, default='Bearer')

    # Fechas de vencimiento de los tokens
    fecha_expiracion_token = models.DateTimeField()
    fecha_expiracion_refresh = models.DateTimeField(blank=True, null=True)

    linked = models.BooleanField(default=False)

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
        db_table = 'vi_reporteredes'

    def __str__(self):
        return f"Reporte del {self.fecha_inicio} al {self.fecha_fin}"


class Post(models.Model):
    cuenta = models.ForeignKey(CuentaRedSocial, on_delete=models.CASCADE, related_name='posts')
    contenido = models.TextField()
    #imagen_url = models.URLField(null=True, blank=True)
    #video_url = models.URLField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    preview = models.URLField(null=True, blank=True)
    media = models.FileField(upload_to= 'posts',null=True, blank=True)

    fecha_publicacion = models.DateField(null=True, blank=True)
    #No mostrar
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_modificacion = models.DateField(auto_now=True)
    
    #usuario_creacion = models.IntegerField()
    #usuario_modificacion = models.IntegerField()
    
    is_programmed = models.BooleanField(default=False)
    programmed_post_time = models.DateTimeField(null=True, blank=True)
    
    ESTADO_CHOICES = [
        ('P', 'Programado'),
        ('Pu', 'Publicado'),
        ('F', 'Fallido'),
        ('B', 'Borrador'),
    ]
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)
    RED_CHOICES = [
        ('TikTok', 'TikTok'),
        ('Facebook', 'Facebook'),
        ('Instagram', 'Instagram'),
    ]
    red_social = models.CharField(max_length=255, choices=RED_CHOICES, default='Facebook')

    tipo = models.CharField(max_length=255, null=True, blank=True)
    id_red_social = models.CharField(max_length=255, null=True, blank=True)
    #is_programmed = models.BooleanField(default=False)  # Agregar este campo

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
        db_table = 'vi_interaccion'

    def __str__(self):
        return f"{self.tipo} de {self.username}"


class Segmento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    criterio = models.TextField()
    fecha_creacion = models.DateField()
    cuenta = models.ForeignKey(CuentaRedSocial, on_delete=models.CASCADE, related_name='segmentos')

    class Meta:
        db_table = 'vi_segmento'

    def __str__(self):
        return self.nombre


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
       db_table = 'vi_etiqueta'

    def __str__(self):
        return self.nombre


class PostEtiqueta(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)

    class Meta:
        db_table = 'vi_postetiqueta'

    def __str__(self):
        return f"Etiqueta: {self.etiqueta.nombre} en Post: {self.post.contenido[:30]}"
