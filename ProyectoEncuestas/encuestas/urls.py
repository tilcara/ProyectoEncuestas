
from django.urls import path
from . import views

app_name='encuestas'

urlpatterns = [
    
    path('', views.IndexView.as_view(), name='index'),

    path('<int:pk>/', views.DetailView.as_view(), name='detalle'),
    
    path('<int:pk>/resultados/', views.ResultadosView.as_view(), name='resultados'),
    
    path('<int:pregunta_id>/votar/', views.votar, name='votar'),
]