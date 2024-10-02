from django.db import models

class Persona(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('DNI', 'DNI'),
        ('RUC', 'RUC'),
        ('CE', 'Carnet de Extranjería'),
    ]
    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = models.CharField(max_length=20, unique=True)
    razon_eliminacion = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()

    def __str__(self):
        return f"{self.tipo_documento}: {self.numero_documento}"

class Usuario(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='usuario')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    con_cuenta = models.BooleanField(default=True)
    numero_telefono = models.CharField(max_length=15, null=True, blank=True)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=100)
    fecha_ultimo_login = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()
    direccion = models.ForeignKey('Direccion', on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.correo})"

class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    esta_activo = models.BooleanField(default=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()

    def __str__(self):
        return self.nombre

class Permiso(models.Model):
    nombre = models.CharField(max_length=50)
    esta_activo = models.BooleanField(default=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()

    def __str__(self):
        return self.nombre

class Notificacion(models.Model):
    ASUNTO_CHOICES = [
        ('ALERTA', 'Alerta'),
        ('INFO', 'Información'),
        ('SISTEMA', 'Sistema'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    asunto = models.CharField(max_length=50, choices=ASUNTO_CHOICES)
    descripcion = models.TextField()
    tipo_notificacion = models.CharField(max_length=50)
    leido = models.BooleanField(default=False)
    esta_activo = models.BooleanField(default=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()

    def __str__(self):
        return f"Notificación para {self.usuario} - {self.asunto}"
    
class Ciudad(models.Model):
    nombre = models.CharField(max_length=100) 
    region = models.CharField(max_length=100)
    esta_activo = models.BooleanField(default=True)
    desactivado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} - {self.region}"

class Ubicacion(models.Model):
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    esta_activo = models.BooleanField(default=True)
    desactivado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()

    def __str__(self):
        return f"Lat: {self.latitud}, Long: {self.longitud}"

class Direccion(models.Model):
    calle = models.CharField(max_length=100)
    numero_exterior = models.CharField(max_length=10)
    numero_interior = models.CharField(max_length=10, null=True, blank=True)
    distrito = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10, null=True, blank=True)
    referencia = models.TextField(null=True, blank=True)
    esta_activo = models.BooleanField(default=True)
    desactivado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()

    def __str__(self):
        return f"{self.calle} {self.numero_exterior}, {self.distrito}"
    
class TipoProducto(models.Model):
    nombre = models.CharField(max_length=100)
    esta_activo = models.BooleanField(default=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()

    def __str__(self):
        return self.nombre

class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100)
    esta_activo = models.BooleanField(default=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()

    def __str__(self):
        return self.nombre

class Fruta(models.Model):
    nombre = models.CharField(max_length=100)
    url_imagen = models.URLField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    esta_activo = models.BooleanField(default=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    precio_a = models.DecimalField(max_digits=10, decimal_places=2)
    precio_b = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_c = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    url_imagen = models.URLField(null=True, blank=True)
    cantidad_min_pedido = models.IntegerField()
    cantidad_max_pedido = models.IntegerField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    informacion_nutricional = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    razon_desactivacion = models.TextField(null=True, blank=True)
    desactivado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()
    se_vende_ecommerce = models.BooleanField(default=True)
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.SET_NULL, null=True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True)
    fruta = models.ForeignKey(Fruta, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre

class ProductoXUsuario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='productos')
    esta_activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()

    def __str__(self):
        return f"Producto {self.producto.nombre} para Usuario {self.usuario.nombre}"