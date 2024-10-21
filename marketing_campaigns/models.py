from django.db import models
from social_management.models import Post, Segmento
from customer_analytics.models import Usuario

class Campana(models.Model):
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=7)
    descripcion = models.TextField()
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ('F', 'Finalizado')
    ]
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    segmentos = models.ManyToManyField(Segmento, related_name='campanas')

    #class Meta:
    #    db_table = 'vi_campana'  # Prefijo 'vi_' para la tabla

    def __str__(self):
        return self.nombre


class CampanaUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE)

    #class Meta:
    #    db_table = 'vi_campana_usuario'  # Prefijo 'vi_' para la tabla

    def __str__(self):
        return f"Usuario {self.usuario.nombre} en campaña {self.campana.nombre}"


class PostCampana(models.Model):
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    #class Meta:
    #    db_table = 'vi_post_campana'  # Prefijo 'vi_' para la tabla

    def __str__(self):
        return f"Post {self.post.id} en campaña {self.campana.nombre}"


class Anuncio(models.Model):
    descripcion = models.TextField()  # TEMPORAL

    #class Meta:
    #    db_table = 'vi_anuncio'  # Prefijo 'vi_' para la tabla

    def __str__(self):
        return f"Anuncio: {self.descripcion[:30]}"
