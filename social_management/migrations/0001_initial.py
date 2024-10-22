# Generated by Django 5.1.1 on 2024-10-22 01:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CuentaRedSocial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=100)),
                ('contraseña', models.CharField(max_length=100)),
                ('token_autenticacion', models.CharField(max_length=255)),
                ('open_id', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_expiracion_token', models.DateField()),
                ('refresh_token', models.CharField(blank=True, max_length=255, null=True)),
                ('tipo_autenticacion', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'vi_cuentaredsocial',
            },
        ),
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'vi_etiqueta',
            },
        ),
        migrations.CreateModel(
            name='RedSocial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('limite_caracteres', models.IntegerField()),
                ('api_url', models.URLField()),
                ('api_version', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'vi_redsocial',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField()),
                ('link', models.URLField(blank=True, null=True)),
                ('preview', models.URLField(blank=True, null=True)),
                ('media', models.FileField(blank=True, null=True, upload_to='posts')),
                ('fecha_publicacion', models.DateField()),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('fecha_modificacion', models.DateField(auto_now=True)),
                ('is_programmed', models.BooleanField(default=False)),
                ('programmed_post_time', models.DateTimeField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('P', 'Programado'), ('Pu', 'Publicado'), ('F', 'Fallido'), ('B', 'Borrador')], max_length=2)),
                ('red_social', models.CharField(choices=[('TikTok', 'TikTok'), ('Facebook', 'Facebook'), ('Instagram', 'Instagram')], default='Facebook', max_length=255)),
                ('tipo', models.CharField(blank=True, max_length=255, null=True)),
                ('id_red_social', models.CharField(blank=True, max_length=255, null=True)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='social_management.cuentaredsocial')),
            ],
            options={
                'db_table': 'vi_post',
            },
        ),
        migrations.CreateModel(
            name='Interaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('C', 'Comentario'), ('M', 'Mención'), ('D', 'Mensaje Directo')], max_length=1)),
                ('contenido', models.TextField()),
                ('fecha', models.DateField()),
                ('username', models.CharField(max_length=100)),
                ('id_interaccion_red_social', models.CharField(blank=True, max_length=255, null=True)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interacciones', to='social_management.cuentaredsocial')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interacciones', to='social_management.post')),
            ],
            options={
                'db_table': 'vi_interaccion',
            },
        ),
        migrations.CreateModel(
            name='PostEtiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiqueta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_management.etiqueta')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_management.post')),
            ],
            options={
                'db_table': 'vi_postetiqueta',
            },
        ),
        migrations.AddField(
            model_name='cuentaredsocial',
            name='red_social',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_management.redsocial'),
        ),
        migrations.CreateModel(
            name='ReporteRedes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('total_usuarios', models.IntegerField()),
                ('total_publicaciones', models.IntegerField()),
                ('total_interacciones', models.IntegerField()),
                ('cuenta_red_social', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_management.cuentaredsocial')),
            ],
            options={
                'db_table': 'vi_reporteredes',
            },
        ),
        migrations.CreateModel(
            name='Segmento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('criterio', models.TextField()),
                ('fecha_creacion', models.DateField()),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='segmentos', to='social_management.cuentaredsocial')),
            ],
            options={
                'db_table': 'vi_segmento',
            },
        ),
    ]
