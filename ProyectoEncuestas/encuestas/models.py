
from django.db import models
from datetime import timedelta
from django.utils import timezone


class Pregunta(models.Model):
	
	pregunta=models.CharField(max_length=200)
	fecha_publicacion=models.DateTimeField('Fecha de Publicacion')

	def publicada_recientemente(self):

		hoy=timezone.now()
		return hoy - timedelta(days=1) <= self.fecha_publicacion <= hoy

	publicada_recientemente.admin_order_field='fecha_publicacion'
	publicada_recientemente.boolean=True
	publicada_recientemente.short_description='¿Publicada recientemente?'

	def __str__(self):

		return self.pregunta


class Opcion(models.Model):
	
	pregunta=models.ForeignKey(Pregunta,on_delete=models.CASCADE)
	opcion=models.CharField(max_length=200)
	votos=models.IntegerField(default=0)

	def __str__(self):
		return self.opcion
