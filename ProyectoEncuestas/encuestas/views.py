

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Pregunta, Opcion


def index(request):
	
	ultimas_preguntas=Pregunta.objects.order_by('-fecha_publicacion')[:5]
	contexto={'ultimas_preguntas':ultimas_preguntas,}
	return render(request,'encuestas/index.html',contexto)	
	
def detalle(request, pregunta_id):

	pregunta=get_object_or_404(Pregunta,pk=pregunta_id)
	return render(request,'encuestas/detalle.html',{'pregunta':pregunta})

def resultados(request, pregunta_id):

	pregunta=get_object_or_404(Pregunta,pk=pregunta_id)
	return render(request,'encuestas/resultados.html',{'pregunta':pregunta})

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