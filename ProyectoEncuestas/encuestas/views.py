from django.http import HttpResponse


def index(request):
    return HttpResponse("Hola mundo. Este es el index de la app encuestas.")