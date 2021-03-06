# Generated by Django 3.0.8 on 2021-11-09 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Atajo', '0002_auto_20211108_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celda',
            name='paquete_semillas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Celda', to='Atajo.PaqueteSemillas'),
        ),
        migrations.AlterField(
            model_name='cultivo',
            name='orden_entrega',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Cultivo', to='Atajo.OrdenEntrega'),
        ),
        migrations.AlterField(
            model_name='cultivo',
            name='parcela',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Cultivo', to='Atajo.Parcela'),
        ),
        migrations.AlterField(
            model_name='imagen',
            name='cultivo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='imagen', to='Atajo.Cultivo'),
        ),
        migrations.AlterField(
            model_name='imagen',
            name='paquete_semillas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='imagen', to='Atajo.PaqueteSemillas'),
        ),
        migrations.AlterField(
            model_name='obrero',
            name='parcela',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Obrero', to='Atajo.Parcela'),
        ),
        migrations.AlterField(
            model_name='ordenentrega',
            name='agricultor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='OrdenEntrega', to='Atajo.Agricultor'),
        ),
        migrations.AlterField(
            model_name='ordenentrega',
            name='parcela',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='OrdenEntrega', to='Atajo.Parcela'),
        ),
        migrations.AlterField(
            model_name='ordenentrega',
            name='transporte',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='OrdenEntrega', to='Atajo.Transporte'),
        ),
        migrations.AlterField(
            model_name='parcela',
            name='agricultor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Parcela', to='Atajo.Agricultor'),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='transporte',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Ruta', to='Atajo.Transporte'),
        ),
    ]
