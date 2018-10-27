

from django.test import TestCase
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from .models import Pregunta, Opcion

# Create your tests here.

class PreguntaModelTests(TestCase):
	
	def test_publicada_recientemente_con_pregunta_futura(self):

		fecha=timezone.now() + timedelta(days=30)
		pregunta_del_futuro=Pregunta(fecha_publicacion=fecha)
		self.assertIs(pregunta_del_futuro.publicada_recientemente(),False)

	def test_publicada_recientemente_con_pregunta_antigua(self):

		fecha=timezone.now() - timedelta(days=1, seconds=1)
		pregunta_antigua=Pregunta(fecha_publicacion=fecha)
		self.assertIs(pregunta_antigua.publicada_recientemente(), False)

	def test_publicada_recientemente_con_pregunta_reciente(self):

		fecha=timezone.now() - timedelta(hours=23, minutes=59)
		pregunta_reciente=Pregunta(fecha_publicacion=fecha)
		self.assertIs(pregunta_reciente.publicada_recientemente(), True)


def crear_pregunta_sin_opcion(pregunta, dias):

	fecha=timezone.now() + timedelta(days=dias)
	return Pregunta.objects.create(pregunta=pregunta,fecha_publicacion=fecha)

def crear_pregunta_con_opcion(pregunta, dias, opcion):

	fecha=timezone.now() + timedelta(days=dias)
	pregunta=Pregunta.objects.create(pregunta=pregunta,fecha_publicacion=fecha)
	pregunta_con_opcion=pregunta.opcion_set.create(opcion=opcion)
	return pregunta_con_opcion.pregunta


class PreguntaIndexViewTests(TestCase):

	def test_no_hay_preguntas(self):

		response=self.client.get(reverse('encuestas:index'))
		self.assertEqual(response.status_code, 200)	
		self.assertContains(response,"No hay encuestas disponibles")
		self.assertQuerysetEqual(response.context['ultimas_preguntas'],[])

	def test_pregunta_del_pasado_con_opcion(self):

		crear_pregunta_con_opcion(pregunta="Pregunta del Pasado con Opcion",dias=-30,opcion="Opcion")
		response=self.client.get(reverse('encuestas:index'))
		self.assertQuerysetEqual(response.context['ultimas_preguntas'],['<Pregunta: Pregunta del Pasado con Opcion>'])

	def test_pregunta_del_pasado_sin_opcion(self):

		crear_pregunta_sin_opcion(pregunta="Pregunta del Pasado sin Opcion",dias=-30)
		response=self.client.get(reverse('encuestas:index'))
		self.assertQuerysetEqual(response.context['ultimas_preguntas'],[])
	
	def test_pregunta_del_futuro(self):

		crear_pregunta_sin_opcion(pregunta="Pregunta del Futuro",dias=30)
		response=self.client.get(reverse('encuestas:index'))			
		self.assertContains(response,"No hay encuestas disponibles")
		self.assertQuerysetEqual(response.context['ultimas_preguntas'],[])

	def test_pregunta_del_futuro_y_pregunta_del_pasado_con_opcion(self):

		crear_pregunta_sin_opcion(pregunta="Pregunta del Futuro",dias=30)
		crear_pregunta_con_opcion(pregunta="Pregunta del Pasado con Opcion",dias=-30,opcion="Opcion")
		response=self.client.get(reverse('encuestas:index'))
		self.assertQuerysetEqual(response.context['ultimas_preguntas'],['<Pregunta: Pregunta del Pasado con Opcion>'])

	def test_pregunta_del_futuro_y_pregunta_del_pasado_sin_opcion(self):

		crear_pregunta_sin_opcion(pregunta="Pregunta del Futuro",dias=30)
		crear_pregunta_sin_opcion(pregunta="Pregunta del Pasado sin Opcion",dias=-30)
		response=self.client.get(reverse('encuestas:index'))
		self.assertQuerysetEqual(response.context['ultimas_preguntas'],[])

	def test_dos_preguntas_del_pasado_con_opcion(self):

		crear_pregunta_con_opcion(pregunta="Pregunta del Pasado con Opcion 1",dias=-30,opcion="Opcion")
		crear_pregunta_con_opcion(pregunta="Pregunta del Pasado con Opcion 2",dias=-5,opcion="Opcion")		
		response=self.client.get(reverse('encuestas:index'))
		self.assertQuerysetEqual(response.context['ultimas_preguntas'],['<Pregunta: Pregunta del Pasado con Opcion 2>','<Pregunta: Pregunta del Pasado con Opcion 1>'])

	def test_dos_preguntas_del_pasado_sin_opcion(self):

		crear_pregunta_sin_opcion(pregunta="Pregunta del Pasado sin Opcion 1",dias=-30)
		crear_pregunta_sin_opcion(pregunta="Pregunta del Pasado sin Opcion 2",dias=-5)		
		response=self.client.get(reverse('encuestas:index'))
		self.assertQuerysetEqual(response.context['ultimas_preguntas'],[])

class PreguntaDetailViewTests(TestCase):
    
    def test_pregunta_del_futuro(self):
        
        pregunta_del_futuro = crear_pregunta_sin_opcion(pregunta='Pregunta del Futuro', dias=5)
        url = reverse('encuestas:detalle', args=(pregunta_del_futuro.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_pregunta_del_pasado_sin_opcion(self):
        
        pregunta_del_pasado = crear_pregunta_sin_opcion('Pregunta del Pasado',-5)
        url = reverse('encuestas:detalle', args=(pregunta_del_pasado.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_pregunta_del_pasado_con_opcion(self):
        
        pregunta_del_pasado = crear_pregunta_con_opcion('Pregunta del Pasado',-5,'Opcion')
        url = reverse('encuestas:detalle', args=(pregunta_del_pasado.id,))
        response = self.client.get(url)
        self.assertContains(response, pregunta_del_pasado.pregunta)