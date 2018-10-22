
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone


class Pregunta(models.Model):
	
	pregunta=models.CharField(max_length=200)
	fecha_publicacion=models.DateTimeField('Fecha de Publicacion')

	def publicada_recientemente(self):
		return self.fecha_publicacion >= timezone.now() - datetime.timedelta(days=1)

	def __str__(self):
		return self.pregunta


class Opcion(models.Model):
	
	pregunta=models.ForeignKey(Pregunta,on_delete=models.CASCADE)
	opcion=models.CharField(max_length=200)
	votos=models.IntegerField(default=0)

	def __str__(self):
		return self.opcion
