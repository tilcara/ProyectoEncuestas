from django.urls import path

from . import views

app_name='encuestas'

urlpatterns = [
    # ej: /encuestas/
    path('', views.index, name='index'),

    # ej: /encuestas/5/
    path('<int:pregunta_id>/', views.detalle, name='detalle'),
    
    # ej: /encuestas/5/resultados/
    path('<int:pregunta_id>/resultados/', views.resultados, name='resultados'),
    
    # ej: /encuestas/5/votar/
    path('<int:pregunta_id>/votar/', views.votar, name='votar'),
]