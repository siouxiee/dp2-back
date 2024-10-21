# Generated by Django 5.1.1 on 2024-10-21 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer_analytics', '0001_initial'),
        ('social_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Campana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=7)),
                ('descripcion', models.TextField()),
                ('presupuesto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo'), ('F', 'Finalizado')], max_length=1)),
                ('segmentos', models.ManyToManyField(related_name='campanas', to='social_management.segmento')),
            ],
        ),
        migrations.CreateModel(
            name='CampanaUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campana', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketing_campaigns.campana')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer_analytics.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='PostCampana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campana', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketing_campaigns.campana')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_management.post')),
            ],
        ),
    ]
