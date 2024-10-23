from django.db import models

class Persona(models.Model):

    id = models.CharField(max_length=50, primary_key=True,db_column='id')  # Corresponde al campo 'id' de la tabla
    tipo_documento = models.CharField(max_length=5, null=True, blank=True,db_column='tipodocumento')  # tipo_documento de longitud 5
    numero_documento = models.CharField(max_length=20, unique=True, null=True, blank=True,db_column='numerodocumento')
    razon_eliminacion = models.CharField(max_length=255, null=True, blank=True,db_column='razoneliminacion')
    estado = models.CharField(max_length=50,db_column='estado')  # Especificar si es un estado textual en vez de booleano
    esta_activo = models.BooleanField(default=True,db_column='estaactivo')
    desactivado_en = models.DateTimeField(null=True, blank=True,db_column='desactivadoen')
    creado_en = models.DateTimeField(auto_now_add=True,db_column='creadoen')
    actualizado_en = models.DateTimeField(auto_now=True,db_column='actualizadoen')
    usuario_creacion = models.CharField(max_length=50,db_column='usuariocreacion') 
    usuario_actualizacion = models.CharField(max_length=50,db_column='usuarioactualizacion') 

    class Meta:
        db_table = 'vi_persona'  # Nombre correcto de la tabla

    def __str__(self):
        return f"{self.tipo_documento}: {self.numero_documento}"

class Rol(models.Model):
    id = models.CharField(max_length=50, primary_key=True,db_column='id')
    nombre = models.CharField(max_length=50,db_column='nombre')
    esta_activo = models.BooleanField(default=True,db_column='estaactivo')
    eliminado_en = models.DateTimeField(null=True, blank=True,db_column='desactivadoen')
    creado_en = models.DateTimeField(auto_now_add=True,db_column='creadoen')
    actualizado_en = models.DateTimeField(auto_now=True,db_column='actualizadoen')
    usuario_creacion = models.IntegerField(db_column='usuariocreacion')
    usuario_actualizacion = models.IntegerField(db_column='usuarioactualizacion')
    
    class Meta:
        db_table = 'vi_rol'

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column='id')
    nombre = models.CharField(max_length=100, db_column='nombre')
    region = models.CharField(max_length=100, db_column='region')
    esta_activo = models.BooleanField(default=True, db_column='estaactivo')
    desactivado_en = models.DateTimeField(null=True, blank=True, db_column='desactivadoen')
    creado_en = models.DateTimeField(auto_now_add=True, db_column='creadoen')
    actualizado_en = models.DateTimeField(auto_now=True, db_column='actualizadoen')
    usuario_creacion = models.CharField(max_length=50, db_column='usuariocreacion')
    usuario_actualizacion = models.CharField(max_length=50, null=True, blank=True, db_column='usuarioactualizacion')

    class Meta:
        db_table = 'vi_ciudad'

    def __str__(self):
        return f"{self.nombre} - {self.region}"

class Ubicacion(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column='id')
    latitud = models.DecimalField(max_digits=9, decimal_places=6, db_column='latitud')
    longitud = models.DecimalField(max_digits=9, decimal_places=6, db_column='longitud')
    esta_activo = models.BooleanField(default=True, db_column='estaactivo')
    desactivado_en = models.DateTimeField(null=True, blank=True, db_column='desactivadoen')
    creado_en = models.DateTimeField(auto_now_add=True, db_column='creadoen')
    actualizado_en = models.DateTimeField(auto_now=True, db_column='actualizadoen')
    usuario_creacion = models.CharField(max_length=50, db_column='usuariocreacion')
    usuario_actualizacion = models.CharField(max_length=50, null=True, blank=True, db_column='usuarioactualizacion')

    class Meta:
        db_table = 'vi_ubicacion'

    def __str__(self):
        return f"Lat: {self.latitud}, Long: {self.longitud}"
    
class Direccion(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column='id')
    calle = models.CharField(max_length=255, db_column='calle')
    numero_exterior = models.CharField(max_length=20, db_column='numeroExterior')
    numero_interior = models.CharField(max_length=20, null=True, blank=True, db_column='numeroInterior')
    distrito = models.CharField(max_length=100, db_column='distrito')
    codigo_postal = models.CharField(max_length=10, null=True, blank=True, db_column='codigoPostal')
    referencia = models.TextField(null=True, blank=True, db_column='referencia')
    id_ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, db_column='id_ciudad')
    id_ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, db_column='id_ubicacion')
    esta_activo = models.BooleanField(default=True, db_column='estaactivo')
    desactivado_en = models.DateTimeField(null=True, blank=True, db_column='desactivadoen')
    creado_en = models.DateTimeField(auto_now_add=True, db_column='creadoen')
    actualizado_en = models.DateTimeField(auto_now=True, db_column='actualizadoen')
    usuario_creacion = models.CharField(max_length=50, db_column='usuariocreacion')
    usuario_actualizacion = models.CharField(max_length=50, null=True, blank=True, db_column='usuarioactualizacion')

    class Meta:
        db_table = 'vi_direccion'

    def __str__(self):
        return f"{self.calle} {self.numero_exterior}, {self.distrito}"

class Usuario(models.Model):
    id = models.CharField(max_length=50, primary_key=True,db_column='id')
    nombre = models.CharField(max_length=100,db_column='nombre')
    apellido = models.CharField(max_length=100,db_column='apellido')
    con_cuenta = models.BooleanField(default=True,db_column='concuenta')
    numero_telefono = models.CharField(max_length=15, null=True, blank=True,db_column='numerotelefono')
    correo = models.EmailField(unique=True,db_column='correo')
    contrasena = models.CharField(max_length=100,db_column='contrasena')
    fecha_ultimo_login = models.DateTimeField(null=True, blank=True,db_column='fechaultimologin')
    id_persona = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column='id_persona')
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='id_rol')
    estaactivo = models.BooleanField(default=True,db_column='estaactivo')
    desactivadoen = models.DateTimeField(null=True, blank=True,db_column='desactivadoen')
    creado_en = models.DateTimeField(auto_now_add=True,db_column='creadoen')
    actualizado_en = models.DateTimeField(auto_now=True,db_column='actualizadoen')
    usuario_creacion = models.IntegerField(db_column='usuariocreacion')
    usuario_actualizacion = models.IntegerField(db_column='usuarioactualizacion')
    direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios',db_column='id')

    class Meta:
        db_table = 'vi_usuario'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.correo})"

class Permiso(models.Model):
    id = models.CharField(max_length=50, primary_key=True,db_column='id')
    nombre = models.CharField(max_length=50,db_column='nombre')
    esta_activo = models.BooleanField(default=True,db_column='estaActivo')
    eliminado_en = models.DateTimeField(null=True, blank=True,db_column='desactivadoen')
    creado_en = models.DateTimeField(auto_now_add=True,db_column='creadoen')
    actualizado_en = models.DateTimeField(auto_now=True,db_column='actualizadoen')
    usuario_creacion = models.IntegerField(db_column='usuariocreacion')
    usuario_actualizacion = models.IntegerField(db_column='usuarioactualizacion')

    class Meta:
        db_table = 'vi_permiso'

    def __str__(self):
        return self.nombre

class Notificacion(models.Model):
    id = models.CharField(max_length=50, primary_key=True,db_column='idNotificacion')
    asunto = models.CharField(max_length=50,db_column='asunto')
    descripcion = models.TextField(db_column='descripcion')
    tipo_notificacion = models.CharField(max_length=50,db_column='tipoNotificacion')
    leido = models.BooleanField(default=False,db_column='leido')
    esta_activo = models.BooleanField(default=True,db_column='estaActivo')
    eliminado_en = models.DateTimeField(null=True, blank=True,db_column='eliminadoEn')
    creado_en = models.DateTimeField(auto_now_add=True,db_column='creadoEn')
    actualizado_en = models.DateTimeField(auto_now=True,db_column='actualizadoEn')
    usuario_creacion = models.IntegerField(db_column='usuarioCreacion')
    usuario_actualizacion = models.IntegerField(db_column='usuarioActualizacion')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,db_column='idUsuario')

    class Meta:
        db_table = 'vi_notificacion'

    def __str__(self):
        return f"Notificación para {self.id_usuario} - {self.asunto}"  

class TipoProducto(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column='id')
    nombre = models.CharField(max_length=255, db_column='nombre')
    esta_activo = models.BooleanField(default=True, db_column='estaactivo')
    eliminado_en = models.DateTimeField(null=True, blank=True, db_column='desactivadoen')
    creado_en = models.DateTimeField(auto_now_add=True, db_column='creadoen')
    actualizado_en = models.DateTimeField(auto_now=True, db_column='actualizadoen')
    usuario_creacion = models.CharField(max_length=50, db_column='usuariocreacion')
    usuario_actualizacion = models.CharField(max_length=50, null=True, blank=True, db_column='usuarioactualizacion')

    class Meta:
        db_table = 'vi_tipoproducto'

    def __str__(self):
        return self.nombre

class Subcategoria(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column='id')
    nombre = models.CharField(max_length=255, db_column='nombre')
    esta_activo = models.BooleanField(default=True, db_column='estaactivo')
    eliminado_en = models.DateTimeField(null=True, blank=True, db_column='desactivadoen')
    creado_en = models.DateTimeField(auto_now_add=True, db_column='creadoen')
    actualizado_en = models.DateTimeField(auto_now=True, db_column='actualizadoen')
    usuario_creacion = models.CharField(max_length=50, db_column='usuariocreacion')
    usuario_actualizacion = models.CharField(max_length=50, null=True, blank=True, db_column='usuarioactualizacion')

    class Meta:
        db_table = 'vi_subcategoria'

    def __str__(self):
        return self.nombre

class Fruta(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column='id')
    nombre = models.CharField(max_length=255, db_column='nombre')
    url_imagen = models.URLField(null=True, blank=True, db_column='urlimagen')
    descripcion = models.TextField(null=True, blank=True, db_column='descripcion')
    esta_activo = models.BooleanField(default=True, db_column='estaactivo')
    informacion_educativa = models.TextField(null=True, blank=True, db_column='informacioneducativa')
    eliminado_en = models.DateTimeField(null=True, blank=True, db_column='desactivadoen')
    creado_en = models.DateTimeField(auto_now_add=True, db_column='creadoen')
    actualizado_en = models.DateTimeField(auto_now=True, db_column='actualizadoen')
    usuario_creacion = models.CharField(max_length=50, db_column='usuariocreacion')
    usuario_actualizacion = models.CharField(max_length=50, null=True, blank=True, db_column='usuarioactualizacion')

    class Meta:
        db_table = 'vi_fruta'

    def __str__(self):
        return self.nombres

class Igv(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column='id')
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, db_column='porcentaje')
    esta_activo = models.BooleanField(default=True, db_column='estaactivo')
    desactivado_en = models.DateTimeField(null=True, blank=True, db_column='desactivadoen')
    creado_en = models.DateTimeField(auto_now_add=True, db_column='creadoen')
    actualizado_en = models.DateTimeField(auto_now=True, db_column='actualizadoen')
    usuario_creacion = models.CharField(max_length=50, db_column='usuariocreacion')
    usuario_actualizacion = models.CharField(max_length=50, null=True, blank=True, db_column='usuarioactualizacion')

    class Meta:
        db_table = 'vi_igv'

    def __str__(self):
        return f"{self.porcentaje}%"

class Producto(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column='id')
    codigo = models.CharField(max_length=255, unique=True, db_column='codigo')
    nombre = models.CharField(max_length=255, db_column='nombre')
    precio_a = models.DecimalField(max_digits=10, decimal_places=2, db_column='precioA')
    precio_b = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='precioB')
    precio_c = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='precioC')
    precio_ecommerce = models.DecimalField(max_digits=10, decimal_places=2, db_column='precioEcommerce')
    url_imagen = models.URLField(null=True, blank=True, db_column='urlImagen')
    descripcion = models.TextField(null=True, blank=True, db_column='descripcion')
    informacion_nutricional = models.TextField(null=True, blank=True, db_column='informacionNutricional')
    razon_eliminacion = models.TextField(null=True, blank=True, db_column='razonEliminacion')
    estado = models.BooleanField(default=True, db_column='estado')
    se_vende_ecommerce = models.BooleanField(default=False, db_column='sevendeEcommerce')
    esta_activo = models.BooleanField(default=True, db_column='estaactivo')
    usuario_creacion = models.CharField(max_length=50, db_column='usuariocreacion')
    usuario_actualizacion = models.CharField(max_length=50, null=True, blank=True, db_column='usuarioactualizacion')
    creado_en = models.DateTimeField(auto_now_add=True, db_column='creadoen')
    actualizado_en = models.DateTimeField(auto_now=True, db_column='actualizadoen')
    desactivado_en = models.DateTimeField(null=True, blank=True, db_column='desactivadoen')
    id_tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.SET_NULL, null=True, db_column='id_tipoproducto')
    id_igv = models.ForeignKey(Igv, on_delete=models.SET_NULL, null=True, db_column='id_igv')
    #subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True)
    #fruta = models.ForeignKey(Fruta, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'vi_producto'

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