

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Pregunta, Opcion


class IndexView(generic.ListView):
	
	template_name='encuestas/index.html'
	context_object_name='ultimas_preguntas'	

	def get_queryset(self):

		return Pregunta.objects.exclude(opcion__opcion__isnull=True).filter(fecha_publicacion__lte=timezone.now()).order_by('-fecha_publicacion')[:5]
	

class DetailView(generic.DetailView):

	model=Pregunta
	template_name='encuestas/detalle.html'

	def get_queryset(self):

		return Pregunta.objects.exclude(opcion__opcion__isnull=True).filter(fecha_publicacion__lte=timezone.now())


class ResultadosView(generic.DetailView):

	model=Pregunta
	template_name='encuestas/resultados.html'


def votar(request, pregunta_id):

	pregunta=get_object_or_404(Pregunta,pk=pregunta_id)
	try:
		opcion_elegida=pregunta.opcion_set.get(pk=request.POST['opcion'])
	except (KeyError, Opcion.DoesNotExist):
		return render(request,'encuestas/detalle.html',{'pregunta':pregunta,'error_message':"No elegiste una opcion",})	
	else:
		opcion_elegida.votos+=1
		opcion_elegida.save()
		return HttpResponseRedirect(reverse('encuestas:resultados',args=(pregunta.id,)))